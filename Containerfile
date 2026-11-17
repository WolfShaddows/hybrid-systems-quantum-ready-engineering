# Purpose: Containerfile. Expected: define local project/tool behavior consumed by its runtime.
# Container lab image; this is a reproducible Linux lab image, not a claim of Red Hat certification.
FROM rust:1.85-slim AS rust-build
WORKDIR /src
COPY rust/Cargo.toml rust/Cargo.lock ./rust/
COPY rust/src ./rust/src
RUN cargo build --release --manifest-path rust/Cargo.toml

FROM maven:3.9.16-eclipse-temurin-21 AS build
RUN apt-get update && apt-get install -y --no-install-recommends gnucobol python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . .
RUN mkdir -p build && cobc -x -free -o build/txn-engine cobol/src/txn_engine.cob \
 && mvn -B -f java/pom.xml package -DskipTests

FROM maven:3.9.16-eclipse-temurin-21
RUN apt-get update && apt-get install -y --no-install-recommends gnucobol && rm -rf /var/lib/apt/lists/* \
 && useradd --uid 10001 --create-home app
WORKDIR /app
COPY --from=build --chown=10001:10001 /src/build/txn-engine /app/build/txn-engine
COPY --from=rust-build --chown=10001:10001 /src/rust/target/release/txn-adapter /app/rust/txn-adapter
COPY --from=rust-build --chown=10001:10001 /src/rust/target/release/libhybrid_rust_adapter.so /app/rust/libhybrid_rust_adapter.so
COPY --from=build --chown=10001:10001 /src/java/target/quarkus-app /app/quarkus-app
RUN mkdir -p /data && chown 10001:0 /data && chmod 0775 /data
ENV COBOL_ENGINE=/app/build/txn-engine \
    RUST_ADAPTER=/app/rust/txn-adapter \
    LEDGER_PATH=/data/transactions.chain \
    QUARKUS_HTTP_HOST=0.0.0.0 \
    QUARKUS_HTTP_PORT=8080
USER 10001
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/quarkus-app/quarkus-run.jar"]




