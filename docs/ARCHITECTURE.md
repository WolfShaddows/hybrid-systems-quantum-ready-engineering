<!-- Purpose: Show conceptual boundaries among research areas and platform components. -->
# Conceptual architecture

```mermaid
flowchart LR
  subgraph SYS[Enterprise modernization]
    COBOL[COBOL: transaction authority] --> API[Java / API: contract and adapter]
    API --> RUST[Rust: bounded native component]
  end
  AI[Local Granite + reproducible evaluation + human review] -. controlled assistance .-> SYS
  subgraph PQC[Post-quantum cryptography on classical systems]
    KEM[ML-KEM · FIPS 203]
    SIG1[ML-DSA · FIPS 204]
    SIG2[SLH-DSA · FIPS 205]
  end
  PQC --> PLATFORM[RHEL / OpenSSL / OpenShift: verify version, protocol, and support]
  subgraph QC[Quantum computing]
    CIRCUITS[Qiskit circuits] --> SIM[Classical simulation with explicit limits]
  end
```

Quantum computing research is separate from PQC. The dotted line represents engineering assistance, never decision authority or deployment approval.
