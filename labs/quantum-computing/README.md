<!-- Purpose: Describe Qiskit experiments, simulation limits, and reproduction metadata. -->
# Quantum computing research with Qiskit

Use Qiskit for small, reproducible experiments with states, measurements, entanglement, and introductory algorithms. No QPU execution or practical advantage is claimed.

1. Bell state: prepare H+CNOT and compare ideal distributions.
2. Three-qubit GHZ: inspect correlations and bitstring conventions.
3. Noise: compare ideal circuits with an explicit Qiskit Aer model and fixed seed.
4. Run a small Deutsch–Jozsa or Grover instance; state oracle, complexity, and limits.
5. Record depth, gates, measurements, simulator backend, seed, version, runtime, and outputs.

Use an isolated environment and pin versions. A classical simulator computes circuit mathematics within resource limits; it is not a QPU and does not fully reproduce physical noise. For hardware runs, record backend, calibration/date, queue, shots, and data policy. See [SOURCES.md](../../references/SOURCES.md).
