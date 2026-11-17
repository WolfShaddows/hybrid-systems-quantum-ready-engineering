<!-- Purpose: Explain the OpenShift deployment workflow, evidence requirements, and limits. -->
# Red Hat / OpenShift deployment lab

OpenShift is a real deployment target for the hybrid transaction API. The cluster builds the Containerfile, runs Quarkus, provides a Service and HTTPS Route, mounts journal storage, and reports readiness/liveness. Quantum hardware is not required: OpenShift workloads and PQC operations use classical systems. Qiskit is a separate classical simulation.

The project has been deployed in Red Hat Developer Sandbox. The latest recorded run is in `data/results/redhat-openshift-deployment.json`; it records OpenShift 4.22.22, build `hybrid-engineering-lab-2` as `Complete`, a ready pod, a bound 1 GiB PVC, successful `/health`, and posted synthetic credit/debit transactions. Treat the JSON as run-specific evidence; Sandbox projects and routes are temporary.

## Run on OpenShift

[Red Hat Developer Sandbox](https://developers.redhat.com/developer-sandbox) is a temporary shared OpenShift environment requiring a Red Hat account and interactive login. The cluster builds the image, so Podman/Docker are not required locally; the OpenShift CLI `oc` is required.

In the Sandbox web console, open **? → Command line tools** to download the Windows `oc` client. Then choose **Copy login command**, run the displayed `oc login` command in PowerShell, and keep its token private. Red Hat documents this [CLI setup flow](https://developers.redhat.com/learn/openshift/download-and-install-red-hat-openshift-cli). From the repository root, run:

```powershell
.\scripts\redhat\deploy-openshift.ps1
```

The script checks authentication and project, starts a binary build from this repository, applies platform resources, configures the Deployment image, waits for readiness, resolves the Route, calls `/health`, submits synthetic transactions, and writes JSON evidence under `data/results/`. Independently inspect with `oc get builds,imagestreams,pods,svc,routes,pvc`.

If a step fails, inspect `oc get events --sort-by=.lastTimestamp` and `oc logs deployment/hybrid-engineering-lab`. Keep failures as evidence; do not claim a successful deployment.

One replica is used because the journal is a local file protected by a process lock, not distributed consensus. A Sandbox run proves only the recorded behavior on that cluster at that time. It does not establish certification, production readiness, RHEL support, or PQC interoperability. The local Windows OpenSSL probe says nothing about Red Hat capabilities.
