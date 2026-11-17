# Purpose: bell state (labs/quantum-computing/bell_state.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
"""Tiny reproducible Qiskit circuit example: a two-qubit Bell state.

Install Qiskit and Qiskit Aer in a dedicated virtual environment. Record exact
package versions and hardware in the experiment record before publishing data.
This is a classical simulation, not a quantum hardware run.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def main() -> None:
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    simulator = AerSimulator()
    compiled = transpile(circuit, simulator, seed_transpiler=7)
    result = simulator.run(compiled, shots=2048, seed_simulator=7).result()

    print("Circuit:")
    print(circuit.draw())
    print("Counts:", result.get_counts())
    print("Expected ideal support: mostly 00 and 11; finite-shot counts vary.")


if __name__ == "__main__":
    main()



