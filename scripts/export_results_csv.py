# Purpose: export results csv (scripts/export_results_csv.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/results"

def emit(name, rows, fields):
    path=OUT/name
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    print(path)
def load(name):
    p=OUT/name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def main():
    g=load("granite-evaluation.json")
    if g:
        emit("granite-evaluation.csv",g.get("records",[]),["model","model_digest","case_id","category","repeat","latency_ms","prompt_tokens","generated_tokens","thinking_mode","raw_answer"])
    q=load("qiskit-circuits.json")
    if q:
        rows=[]
        for r in q.get("results",[]):
            rows.append({**r,"operations_json":json.dumps(r.get("operations",{}),sort_keys=True),"counts_json":json.dumps(r.get("counts",{}),sort_keys=True),"noise_model_json":json.dumps(r.get("noise_model",{}),sort_keys=True)})
        emit("qiskit-circuits.csv",rows,["name","qubits","depth","shots","elapsed_ms","backend","pass","operations_json","counts_json","noise_model_json"])
    p=load("pqc-openssl-capabilities.json")
    if p:
        rows=[{"algorithm":name,"detected":found,"openssl_version":p.get("openssl_version_output","").splitlines()[0],"probe_status":p.get("status"),"operation_tests":p.get("algorithm_operation_tests"),"fips_validation":p.get("fips_validation")} for name,found in p.get("algorithms_detected",{}).items()]
        emit("pqc-openssl-capabilities.csv",rows,["algorithm","detected","openssl_version","probe_status","operation_tests","fips_validation"])
    b=load("enterprise-benchmark.json")
    if b:
        rows=[{"metric":"requests","value":b.get("requests"),"unit":"count"},{"metric":"duration","value":b.get("duration_s"),"unit":"seconds"},{"metric":"throughput","value":b.get("throughput_rps"),"unit":"requests/second"}]
        rows += [{"metric":"latency_"+k,"value":v,"unit":"milliseconds"} for k,v in b.get("latency_ms",{}).items()]
        emit("enterprise-benchmark.csv",rows,["metric","value","unit"])
    smoke=load("quarkus-smoke.json")
    if smoke:
        emit("quarkus-smoke.csv",[{"operation":x.get("operation"),"status":x.get("status"),"balance_cents":x.get("balance_cents"),"replayed":x.get("replayed")} for x in smoke.get("transactions",[])],["operation","status","balance_cents","replayed"])
if __name__=="__main__": main()



