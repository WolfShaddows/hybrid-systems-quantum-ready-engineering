<!-- Purpose: Define PQC concepts, test procedure, and compatibility evidence requirements. -->
# Post-quantum cryptography (PQC)

- **ML-KEM (FIPS 203):** key encapsulation for establishing a shared secret.
- **ML-DSA (FIPS 204):** lattice-based digital signature.
- **SLH-DSA (FIPS 205):** stateless hash-based signature.
- **Crypto agility:** controlled, auditable ability to identify and replace algorithms/protocols.
- **Hybrid:** a defined composition in a specific protocol. Concatenating bytes is not a secure composition.

PQC runs on classical systems. Qiskit circuits do not validate PQC; PQC tests do not demonstrate quantum computing.

Inventory TLS, SSH, PKI, code signing, VPN, and storage. Prioritize exposure, data lifetime, criticality, and replacement difficulty. Select protocol and implementation versions; record formats, negotiation, fallback, and downgrade behavior. Test interoperability and rotation; measure sizes, handshake, CPU, memory, latency, and failures. Review FIPS/support status and migration/rollback.

Do not implement primitives or invent hybrid schemes. Algorithm availability does not imply TLS, certificate, firmware, FIPS, or managed-service support.

| Product/version | Algorithm | Protocol | Mode | Client/server | Official support | Result/date |
|---|---|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending | Pending | Not tested |

See FIPS 203/204/205 and NIST SP 800-227 in [SOURCES.md](../../references/SOURCES.md).
