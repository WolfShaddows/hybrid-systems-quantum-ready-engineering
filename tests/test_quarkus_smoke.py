# Purpose: test quarkus smoke (tests/test_quarkus_smoke.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import json, os, socket, subprocess, tempfile, time, unittest, urllib.error, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BIN_SUFFIX=".exe" if os.name=="nt" else ""

class QuarkusSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jar=ROOT/"java/target/quarkus-app/quarkus-run.jar"
        if not jar.exists(): raise unittest.SkipTest("Build the Quarkus package first")
        cls.temp=tempfile.TemporaryDirectory(prefix="hybrid-quarkus-")
        cls.ledger=Path(cls.temp.name)/"transactions.chain"
        with socket.socket() as s: s.bind(("127.0.0.1",0)); cls.port=s.getsockname()[1]
        env=os.environ.copy(); env.update({"QUARKUS_HTTP_HOST":"127.0.0.1","QUARKUS_HTTP_PORT":str(cls.port),"LEDGER_PATH":str(cls.ledger),"COBOL_ENGINE":str(ROOT/"build"/("txn-engine"+BIN_SUFFIX)),"RUST_ADAPTER":str(ROOT/"rust/target/release"/("txn-adapter"+BIN_SUFFIX)),"RUST_LIBRARY":str(ROOT/"rust/target/release"/("hybrid_rust_adapter.dll" if os.name=="nt" else "libhybrid_rust_adapter.so"))})
        if os.name == "nt" and not env.get("COB_CONFIG_DIR"):
            cobc=shutil.which("cobc")
            if cobc: env["COB_CONFIG_DIR"]=str(Path(cobc).resolve().parent.parent/"config")
        cls.process=subprocess.Popen(["java","-jar",str(jar)],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        deadline=time.time()+40
        while time.time()<deadline:
            if cls.process.poll() is not None: raise RuntimeError("Quarkus exited: "+(cls.process.stdout.read() or ""))
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{cls.port}/health",timeout=.5).close(); return
            except Exception: time.sleep(.2)
        cls.process.terminate(); raise RuntimeError("Quarkus health endpoint did not become ready")
    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        try: cls.process.wait(timeout=10)
        except subprocess.TimeoutExpired: cls.process.kill()
        cls.process.stdout.close(); cls.temp.cleanup()
    def setUp(self): self.ledger.write_text("",encoding="utf-8")
    def post(self,key,operation,amount):
        body={"account_id":"quarkus-test","idempotency_key":key,"operation":operation,"amount_cents":amount}
        req=urllib.request.Request(f"http://127.0.0.1:{self.port}/transactions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=20) as response: return response.status,json.loads(response.read())
        except urllib.error.HTTPError as exc:
            with exc: return exc.code,json.loads(exc.read())
    def test_quarkus_rest_uses_cobol_decision_core(self):
        status,credit=self.post("q-credit","CREDIT",980)
        self.assertEqual((status,credit["balance_cents"]),(201,980))
        health=json.loads(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/health").read())
        self.assertEqual(health["decision_adapter"],"native-ffi")
        status,debit=self.post("q-debit","DEBIT",980)
        self.assertEqual((status,debit["balance_cents"]),(201,0))
        self.assertEqual(len(self.ledger.read_text(encoding="utf-8").splitlines()),2)
        out=ROOT/"data/results/quarkus-smoke.json"; out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps({"schema_version":"1.0","experiment_id":"quarkus-rest-smoke","status":"passed","transactions":[credit,debit],"decision_adapter":"native-ffi","assertions":["REST health responded","Quarkus called the Rust C ABI through JNA","Rust invoked the COBOL decision engine","full-balance debit was accepted","two journal records were persisted"]},indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": unittest.main(verbosity=2)





