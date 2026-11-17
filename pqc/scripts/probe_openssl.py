# Purpose: probe openssl (pqc/scripts/probe_openssl.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import json, os, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OPENSSL=os.environ.get("OPENSSL_BIN","openssl")
def run(args):
    try:
        p=subprocess.run([OPENSSL,*args],capture_output=True,text=True,timeout=15)
        return {"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
    except Exception as exc:
        return {"exit_code":None,"stdout":"","stderr":str(exc)}
def main():
    version=run(["version","-a"])
    kem=run(["list","-kem-algorithms"])
    sig=run(["list","-signature-algorithms"])
    ktext=kem["stdout"]+kem["stderr"]; stext=sig["stdout"]+sig["stderr"]
    algorithms={
      "ML-KEM-512":bool(re.search(r"ML[-_]KEM[-_]512",ktext,re.I)),
      "ML-KEM-768":bool(re.search(r"ML[-_]KEM[-_]768",ktext,re.I)),
      "ML-KEM-1024":bool(re.search(r"ML[-_]KEM[-_]1024",ktext,re.I)),
      "ML-DSA":bool(re.search(r"ML[-_]DSA",stext,re.I)),
      "SLH-DSA":bool(re.search(r"SLH[-_]DSA",stext,re.I)),
    }
    payload={"schema_version":"1.0","experiment_id":"openssl-pqc-capability-probe","status":"executed","timestamp_utc":datetime.now(timezone.utc).isoformat(),"openssl_version_output":version["stdout"].strip() or version["stderr"].strip(),"commands":{"kem_list":{"exit_code":kem["exit_code"],"stderr":kem["stderr"].strip()},"signature_list":{"exit_code":sig["exit_code"],"stderr":sig["stderr"].strip()}},"providers":"not inferred by this capability probe","algorithms_detected":algorithms,"algorithm_operation_tests":"not run; this probe detects availability only","fips_validation":"not evaluated","limitations":["algorithm listing does not prove protocol interoperability, FIPS validation, side-channel resistance, or production support"]}
    if not any(algorithms.values()): payload["status"]="executed_no_pqc_algorithms_detected"
    out=ROOT/"data/results/pqc-openssl-capabilities.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8"); print(json.dumps(payload,indent=2))
if __name__=="__main__": main()




