<!-- Purpose: Explain the Quarkus REST API, transaction core, and build/run commands. -->
# Quarkus REST API

The REST service uses Quarkus and delegates to the same transaction core as the dependency-free JDK adapter. Both front ends exercise the same Rust/COBOL decision and journal code.

From the repository root, build with `..\..\mvnw.cmd -f java\pom.xml package` or run `scripts\run-quarkus.ps1`. JDK 21+ and network access are needed the first time Maven resolves Quarkus artifacts. Bootstrap Maven locally with `scripts\bootstrap-maven.ps1`.

Endpoints: `GET /health` and `POST /transactions`. The sample OpenShift deployment uses one replica because a local file-journal lock is not distributed consensus or replication.
