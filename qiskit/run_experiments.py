# Purpose: run experiments (qiskit/run_experiments.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
from __future__ import annotations
import json, platform, time
from pathlib import Path
import qiskit, qiskit_aer
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results" / "qiskit-circuits.json"
SEED = 20261117
SHOTS = 4096

def execute(name, circuit, backend, seed):
    started = time.perf_counter()
    compiled = transpile(circuit, backend, seed_transpiler=seed)
    result = backend.run(compiled, shots=SHOTS, seed_simulator=seed).result()
    counts = result.get_counts()
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {"name":name,"qubits":circuit.num_qubits,"depth":circuit.depth(),"operations":dict(circuit.count_ops()),
            "shots":SHOTS,"counts":counts,"elapsed_ms":round(elapsed_ms,3),"backend":backend.name}

def main():
    ideal = AerSimulator(seed_simulator=SEED)
    records=[]
    bell=QuantumCircuit(2,2); bell.h(0); bell.cx(0,1); bell.measure([0,1],[0,1])
    bell_result=execute("bell_2q_ideal",bell,ideal,SEED)
    bell_result["pass"] = set(bell_result["counts"]).issubset({"00","11"}) and set(bell_result["counts"])=={"00","11"}
    records.append(bell_result)

    ghz=QuantumCircuit(3,3); ghz.h(0)
    for i in range(2): ghz.cx(i,i+1)
    ghz.measure(range(3),range(3))
    ghz_result=execute("ghz_3q_ideal",ghz,ideal,SEED+1)
    ghz_result["pass"] = set(ghz_result["counts"])=={"000","111"}
    records.append(ghz_result)

    # Two-qubit Grover search for |11>, one Grover iteration.
    grover=QuantumCircuit(2,2); grover.h([0,1]); grover.cz(0,1); grover.h([0,1]); grover.x([0,1]); grover.cz(0,1); grover.x([0,1]); grover.h([0,1]); grover.measure([0,1],[0,1])
    grover_result=execute("grover_mark_11_2q_ideal",grover,ideal,SEED+2)
    grover_result["pass"] = grover_result["counts"].get("11",0) >= int(SHOTS*0.98)
    records.append(grover_result)

    noise=NoiseModel(); noise.add_all_qubit_quantum_error(depolarizing_error(0.02,1),["h"]); noise.add_all_qubit_quantum_error(depolarizing_error(0.03,2),["cx"])
    noisy=execute("bell_2q_depolarizing_noise",bell,AerSimulator(noise_model=noise),SEED+3)
    noisy["noise_model"]={"single_qubit_depolarizing_probability":0.02,"two_qubit_depolarizing_probability":0.03}
    noisy["expected_relation"]="correlated 00/11 outcomes remain dominant; noise may introduce 01/10"
    noisy["pass"] = noisy["counts"].get("00",0)+noisy["counts"].get("11",0) > SHOTS/2
    records.append(noisy)

    scaling=[]
    for n in [2,4,8,12]:
        qc=QuantumCircuit(n,n); qc.h(0)
        for i in range(n-1): qc.cx(i,i+1)
        qc.measure(range(n),range(n))
        rec=execute(f"ghz_{n}q_scaling",qc,ideal,SEED+n)
        rec["pass"] = set(rec["counts"]).issubset({"0"*n,"1"*n})
        scaling.append(rec)
    payload={"schema_version":"1.0","experiment_id":"qiskit-circuit-basics","status":"executed","environment":{"python":platform.python_version(),"qiskit":qiskit.__version__,"qiskit_aer":qiskit_aer.__version__,"platform":platform.platform()},"seed":SEED,"results":records+scaling,"limitations":["classical Aer simulation only; no QPU execution","ideal statevector results do not model hardware calibration","runtime depends on this host"]}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2))
    if not all(r["pass"] for r in records+scaling): raise SystemExit(1)

if __name__=="__main__": main()




