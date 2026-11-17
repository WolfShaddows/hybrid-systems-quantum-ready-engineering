<!-- Purpose: Define the OpenShift deployment experiment and separate PQC capability assessment. -->
# Red Hat ecosystem: OpenShift, RHEL, and OpenSSL

## Research question

Can the transaction API run as a real OpenShift workload with platform health checks, routing, storage, and independent evidence, without quantum hardware?

**Yes.** OpenShift runs on classical compute. Qiskit Aer is a separate simulation. A platform claim requires a successful deployment on an accessible cluster; a manifest alone is not evidence.

## Deployment path

Use Red Hat Developer Sandbox or another authorized OpenShift cluster. The cluster builds the image from the repository Containerfile, so a local container engine is not required. An authenticated `oc` CLI session is required.

From the repository root, run `.\scripts\redhat\deploy-openshift.ps1` after interactive login. It creates a binary build, uploads source, waits for the image, applies Deployment/Service/Route/PVC, waits for pod readiness, checks `/health`, submits synthetic transactions, and saves cluster version, image digest, pod, route, results, timestamp, and exit statuses in `data/results/redhat-openshift-deployment.json`.

A Sandbox run demonstrates only behavior on that cluster. It does not certify the software, prove production readiness, or establish RHEL/OpenSSL behavior. The single-replica journal is not a distributed ledger.

## Separate PQC support matrix

| Component | Exact version | Capability | Provider/configuration | FIPS/support limit | Source/date | Test |
|---|---|---|---|---|---|---|
| RHEL | Pending | Pending | Pending | Pending | Pending | Not run |
| OpenSSL | Pending | Pending | Pending | Pending | Pending | Not run |
| OpenShift | Pending | Pending | Pending | Pending | Pending | Not run |

Freeze exact minor versions and policy. Test algorithm listing, actual operation, encoding, protocol negotiation, interoperability, and FIPS mode separately. Never infer OpenShift behavior from RHEL.
