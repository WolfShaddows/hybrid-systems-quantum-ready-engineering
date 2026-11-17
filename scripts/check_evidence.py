# Purpose: check evidence (scripts/check_evidence.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data/results"
summary=json.loads((OUT/"verification-summary.json").read_text(encoding="utf-8"))
checks=[]
for item in summary["artifacts"]:
    path=OUT/item["file"]
    raw=path.read_bytes()
    actual=hashlib.sha256(raw).hexdigest()
    if actual!=item["sha256"]: raise SystemExit(f"FAIL hash mismatch: {item['file']}")
    data=json.loads(raw)
    if data.get("experiment_id")!=item["experiment_id"] or data.get("status")!=item["status"]: raise SystemExit(f"FAIL metadata mismatch: {item['file']}")
    checks.append(item["file"])
q=json.loads((OUT/"qiskit-circuits.json").read_text(encoding="utf-8"))
if len(q.get("results",[]))!=8 or not all(x.get("pass") for x in q["results"]): raise SystemExit("FAIL Qiskit result assertions")
s=json.loads((OUT/"quarkus-smoke.json").read_text(encoding="utf-8"))
if s.get("decision_adapter")!="native-ffi" or len(s.get("transactions",[]))!=2: raise SystemExit("FAIL Quarkus FFI smoke evidence")
g=json.loads((OUT/"granite-evaluation.json").read_text(encoding="utf-8"))
if len(g.get("records",[]))!=12 or len(g.get("models",[]))!=2: raise SystemExit("FAIL Granite record count")
p=json.loads((OUT/"pqc-openssl-capabilities.json").read_text(encoding="utf-8"))
if any(p.get("algorithms_detected",{}).values()): raise SystemExit("FAIL documented local PQC absence changed; review conclusion")
rh=json.loads((OUT/"redhat-openshift-deployment.json").read_text(encoding="utf-8"))
if rh.get("status")!="passed" or rh.get("build",{}).get("phase")!="Complete": raise SystemExit("FAIL OpenShift deployment or image build evidence")
if not rh.get("pod") or not any(pod.get("ready") and pod.get("phase")=="Running" for pod in rh["pod"]): raise SystemExit("FAIL no ready OpenShift pod recorded")
if rh.get("pvc",{}).get("phase")!="Bound" or rh.get("health",{}).get("status")!="ok": raise SystemExit("FAIL OpenShift storage or health evidence")
if [t.get("balance_cents") for t in rh.get("transactions",[])]!=[700,450]: raise SystemExit("FAIL OpenShift transaction balances")
print(f"PASS: {len(checks)} evidence hashes and Qiskit/Quarkus/Granite/PQC assertions; artifacts={', '.join(checks)}")



