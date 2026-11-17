# Purpose: benchmark (scripts/benchmark.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import json, os, platform, shutil, statistics, subprocess, tempfile, time, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUFFIX=".exe" if os.name=="nt" else ""
PORT=int(os.environ.get("PORT","18080"))
with tempfile.TemporaryDirectory(prefix="hybrid-bench-") as tmp:
    env=os.environ.copy()
    env.update({"PORT":str(PORT),"HOST":"127.0.0.1","LEDGER_PATH":str(Path(tmp)/"transactions.chain"),"RUST_ADAPTER":str(ROOT/"rust/target/release"/("txn-adapter"+SUFFIX)),"COBOL_ENGINE":str(ROOT/"build"/("txn-engine"+SUFFIX))})
    if os.name=="nt" and not env.get("COB_CONFIG_DIR"):
        cobc=shutil.which("cobc")
        if cobc: env["COB_CONFIG_DIR"]=str(Path(cobc).resolve().parent.parent/"config")
    server=subprocess.Popen(["java","-cp",str(ROOT/"build/java"),"org.hybridlab.Main"],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        url=f"http://127.0.0.1:{PORT}/transactions"
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health",timeout=.2).close(); break
            except Exception: time.sleep(.1)
        samples=[]; start=time.perf_counter(); n=int(os.environ.get("BENCH_REQUESTS","100"))
        for i in range(n):
            body=json.dumps({"account_id":"bench","idempotency_key":f"bench-{i}","operation":"CREDIT","amount_cents":1}).encode()
            req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"},method="POST")
            t=time.perf_counter(); urllib.request.urlopen(req,timeout=15).read(); samples.append((time.perf_counter()-t)*1000)
        duration=time.perf_counter()-start
        result={"schema_version":"1.0","experiment_id":"benchmark-enterprise-api","status":"executed","environment":{"os":platform.platform(),"python":platform.python_version()},"requests":n,"duration_s":round(duration,6),"throughput_rps":round(n/duration,3),"latency_ms":{"min":round(min(samples),3),"p50":round(statistics.median(samples),3),"p95":round(sorted(samples)[int(.95*(n-1))],3),"max":round(max(samples),3)},"cpu_percent":None,"memory_bytes":None,"limitations":["single local process; no network or TLS; OS CPU/RAM not sampled by this script"]}
        out=ROOT/"data/results/enterprise-benchmark.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print(json.dumps(result,indent=2))
    finally:
        server.terminate(); server.wait(timeout=5)





