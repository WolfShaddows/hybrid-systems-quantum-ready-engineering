// Purpose: Main (java/src/main/java/org/hybridlab/Main.java). Expected: validate API input, coordinate decisions and journal, and return a structured response.
package org.hybridlab;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.security.MessageDigest;
import java.util.HashMap;
import java.util.HexFormat;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
import java.util.regex.Pattern;

public final class Main {
    private static final long MAX_BALANCE = 999_999_999_999_999_999L;
    private static final long MAX_AMOUNT = 999_999_999L;
    private static final String GENESIS = "0".repeat(64);
    private static final Pattern IDENTIFIER = Pattern.compile("[A-Za-z0-9_-]{1,64}");
    private static final ReentrantLock JVM_LOCK = new ReentrantLock();
    private static final Path LEDGER = Path.of(System.getenv().getOrDefault("LEDGER_PATH", "data/transactions.chain")).toAbsolutePath();
    private static final Path LOCK = Path.of(LEDGER + ".lock");
    private static final Path ADAPTER = Path.of(System.getenv().getOrDefault("RUST_ADAPTER", "rust/target/release/txn-adapter.exe")).toAbsolutePath();
    private static final Path COBOL = Path.of(System.getenv().getOrDefault("COBOL_ENGINE", "build/txn-engine.exe")).toAbsolutePath();

    private Main() {}

    // Stage 1: initialize the ledger path, REST endpoints, worker pool, and graceful shutdown.
    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        String host = System.getenv().getOrDefault("HOST", "127.0.0.1");
        Files.createDirectories(LEDGER.getParent());
        HttpServer server = HttpServer.create(new java.net.InetSocketAddress(host, port), 128);
        server.createContext("/health", exchange -> respond(exchange, 200,
                "{\"status\":\"ok\",\"ledger\":\"append-only-hash-chain\",\"single_writer_lock\":true,\"decision_adapter\":\"" + (System.getenv("RUST_LIBRARY") == null ? "process" : "native-ffi") + "\"}"));
        server.createContext("/transactions", Main::handleTransactions);
        server.setExecutor(Executors.newFixedThreadPool(8));
        Runtime.getRuntime().addShutdownHook(new Thread(() -> server.stop(1)));
        server.start();
        System.out.printf("LISTENING http://%s:%d%n", host, port);
    }

    public record ApiResponse(int status, String body) {}

    // Stage 2: parse and validate the request, execute the transaction, then map domain failures to HTTP codes.
    public static ApiResponse submitJson(String json) {
        try {
            Request request = Request.parse(json);
            Result result = transact(request);
            int status = result.replayed ? 200 : (result.status.startsWith("REJECTED_") ? 422 : 201);
            return new ApiResponse(status, result.toJson(request));
        } catch (BadRequest e) { return new ApiResponse(400, error(e.getMessage())); }
          catch (Conflict e) { return new ApiResponse(409, error(e.getMessage())); }
          catch (LedgerCorruption e) { return new ApiResponse(503, error("ledger_integrity_failure")); }
          catch (DecisionFailure e) { return new ApiResponse(502, error("transaction_decision_unavailable")); }
          catch (IOException e) { return new ApiResponse(500, error("ledger_io_failure")); }
          catch (InterruptedException e) { Thread.currentThread().interrupt(); return new ApiResponse(503, error("transaction_interrupted")); }
    }

    private static void handleTransactions(HttpExchange exchange) throws IOException {
        if (!"POST".equals(exchange.getRequestMethod())) { respond(exchange, 405, error("method_not_allowed")); return; }
        byte[] bytes = exchange.getRequestBody().readNBytes(4097);
        if (bytes.length > 4096) { respond(exchange, 413, error("request_too_large")); return; }
        ApiResponse result = submitJson(new String(bytes, StandardCharsets.UTF_8));
        respond(exchange, result.status(), result.body());
    }
    // Stage 3: hold process and file locks, replay idempotent requests, call the decision chain, verify arithmetic, and append one durable hash-linked event.
    private static Result transact(Request request) throws IOException, InterruptedException, BadRequest, Conflict, LedgerCorruption, DecisionFailure {
        JVM_LOCK.lock();
        try {
            Files.createDirectories(LEDGER.getParent());
            try (FileChannel lockChannel = FileChannel.open(LOCK, StandardOpenOption.CREATE, StandardOpenOption.WRITE);
                 FileLock ignored = lockChannel.lock()) {
                // Verify the existing hash chain before deriving the current account balance.
                Journal journal = Journal.read(LEDGER);
                Event prior = journal.byKey.get(request.idempotencyKey);
                if (prior != null) {
                    if (!prior.account.equals(request.accountId) || !prior.operation.equals(request.operation)
                            || prior.amount != request.amountCents) throw new Conflict("idempotency_key_conflict");
                    return new Result("REPLAY", prior.balance, true);
                }
                long current = journal.balances.getOrDefault(request.accountId, 0L);
                // The native/process adapter returns COBOL's business decision; Java independently checks it below.
                String decision = runAdapter(request, current);
                String[] fields = decision.split("\\|", -1);
                if (fields.length != 2) throw new DecisionFailure();
                String status = fields[0];
                long proposed;
                try { proposed = Long.parseLong(fields[1]); } catch (NumberFormatException ex) { throw new DecisionFailure(); }
                long expected;
                String expectedStatus;
                if ("DEBIT".equals(request.operation) && request.amountCents > current) {
                    expectedStatus = "REJECTED_INSUFFICIENT_FUNDS";
                    expected = current;
                } else if ("CREDIT".equals(request.operation) && current > MAX_BALANCE - request.amountCents) {
                    expectedStatus = "REJECTED_BALANCE_OVERFLOW";
                    expected = current;
                } else {
                    expectedStatus = "POSTED";
                    expected = "CREDIT".equals(request.operation) ? current + request.amountCents : current - request.amountCents;
                }
                if (!expectedStatus.equals(status) || expected != proposed) throw new DecisionFailure();
                if (status.startsWith("REJECTED_")) return new Result(status, current, false);
                String body = request.accountId + "|" + request.idempotencyKey + "|" + request.operation + "|"
                        + request.amountCents + "|" + proposed;
                // Link the new event to its predecessor and force the append to durable storage.
                String line = body + "|" + journal.lastHash + "|" + sha256(journal.lastHash + "|" + body) + "\n";
                try (FileChannel channel = FileChannel.open(LEDGER, StandardOpenOption.CREATE, StandardOpenOption.WRITE, StandardOpenOption.APPEND)) {
                    ByteBuffer buffer = StandardCharsets.UTF_8.encode(line);
                    while (buffer.hasRemaining()) channel.write(buffer);
                    channel.force(true);
                }
                return new Result(status, proposed, false);
            }
        } finally { JVM_LOCK.unlock(); }
    }

    private static String runAdapter(Request request, long balance) throws IOException, InterruptedException, DecisionFailure {
        if (System.getenv("RUST_LIBRARY") != null) {
            try {
                Class<?> adapter = Class.forName("org.hybridlab.NativeAdapter");
                return (String) adapter.getMethod("decide", String.class, String.class, long.class, long.class)
                        .invoke(null, request.accountId, request.operation, request.amountCents, balance);
            } catch (ReflectiveOperationException e) { throw new DecisionFailure(); }
        }
        ProcessBuilder builder = new ProcessBuilder(ADAPTER.toString(), request.accountId, request.operation,
                Long.toString(request.amountCents), Long.toString(balance));
        builder.environment().put("COBOL_ENGINE", COBOL.toString());
        builder.redirectErrorStream(false);
        Process process = builder.start();
        if (!process.waitFor(10, TimeUnit.SECONDS)) {
            process.destroyForcibly();
            throw new DecisionFailure();
        }
        byte[] out = process.getInputStream().readNBytes(256);
        if (process.exitValue() != 0) throw new DecisionFailure();
        return new String(out, StandardCharsets.UTF_8).trim();
    }

    private static String sha256(String value) {
        try { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8))); }
        catch (Exception e) { throw new IllegalStateException(e); }
    }

    private static void respond(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.getResponseHeaders().set("Cache-Control", "no-store");
        exchange.sendResponseHeaders(status, bytes.length);
        try (var output = exchange.getResponseBody()) { output.write(bytes); }
    }

    private static String error(String code) { return "{\"error\":\"" + code + "\"}"; }

    private record Request(String accountId, String idempotencyKey, String operation, long amountCents) {
        static Request parse(String json) throws BadRequest {
            Map<String, String> fields = FlatJson.parse(json);
            if (!fields.keySet().equals(java.util.Set.of("account_id", "idempotency_key", "operation", "amount_cents")))
                throw new BadRequest("invalid_fields");
            String account = fields.get("account_id");
            String key = fields.get("idempotency_key");
            String operation = fields.get("operation");
            String amountText = fields.get("amount_cents");
            if (!IDENTIFIER.matcher(account).matches() || account.length() > 32 || !IDENTIFIER.matcher(key).matches())
                throw new BadRequest("invalid_identifier");
            if (!"CREDIT".equals(operation) && !"DEBIT".equals(operation)) throw new BadRequest("invalid_operation");
            long amount;
            try { amount = Long.parseLong(amountText); } catch (NumberFormatException e) { throw new BadRequest("invalid_amount"); }
            if (amount < 1 || amount > MAX_AMOUNT) throw new BadRequest("amount_out_of_range");
            return new Request(account, key, operation, amount);
        }
    }

    private record Event(String account, String key, String operation, long amount, long balance) {}
    private record Journal(Map<String, Long> balances, Map<String, Event> byKey, String lastHash) {
        static Journal read(Path path) throws IOException, LedgerCorruption {
            Map<String, Long> balances = new HashMap<>();
            Map<String, Event> byKey = new HashMap<>();
            String previous = GENESIS;
            if (Files.exists(path)) {
                for (String line : Files.readAllLines(path, StandardCharsets.UTF_8)) {
                    String[] f = line.split("\\|", -1);
                    if (f.length != 7) throw new LedgerCorruption();
                    String body = String.join("|", f[0], f[1], f[2], f[3], f[4]);
                    if (!f[5].equals(previous) || !f[6].equals(sha256(previous + "|" + body))) throw new LedgerCorruption();
                    long amount, after;
                    try { amount = Long.parseLong(f[3]); after = Long.parseLong(f[4]); } catch (NumberFormatException e) { throw new LedgerCorruption(); }
                    if (!IDENTIFIER.matcher(f[0]).matches() || !IDENTIFIER.matcher(f[1]).matches()
                            || (!"CREDIT".equals(f[2]) && !"DEBIT".equals(f[2])) || amount < 1 || amount > MAX_AMOUNT) throw new LedgerCorruption();
                    long before = balances.getOrDefault(f[0], 0L);
                    long computed;
                    if ("CREDIT".equals(f[2])) {
                        if (before > MAX_BALANCE - amount) throw new LedgerCorruption();
                        computed = before + amount;
                    } else {
                        if (amount > before) throw new LedgerCorruption();
                        computed = before - amount;
                    }
                    if (computed != after || byKey.containsKey(f[1])) throw new LedgerCorruption();
                    Event event = new Event(f[0], f[1], f[2], amount, after);
                    byKey.put(f[1], event);
                    balances.put(f[0], after);
                    previous = f[6];
                }
            }
            return new Journal(balances, byKey, previous);
        }
    }

    private record Result(String status, long balance, boolean replayed) {
        String toJson(Request request) {
            return "{\"status\":\"" + status + "\",\"account_id\":\"" + request.accountId
                    + "\",\"idempotency_key\":\"" + request.idempotencyKey + "\",\"operation\":\""
                    + request.operation + "\",\"amount_cents\":" + request.amountCents
                    + ",\"balance_cents\":" + balance + ",\"replayed\":" + replayed + "}";
        }
    }

    private static final class FlatJson {
        private final String text; private int i;
        private FlatJson(String text) { this.text = text; }
        static Map<String, String> parse(String text) throws BadRequest {
            FlatJson p = new FlatJson(text); Map<String, String> out = new HashMap<>();
            p.ws(); p.take('{'); p.ws();
            if (p.peek('}')) throw new BadRequest("empty_request");
            while (true) {
                String key = p.string(); p.ws(); p.take(':'); p.ws();
                String value = p.peek('"') ? p.string() : p.number();
                if (out.putIfAbsent(key, value) != null) throw new BadRequest("duplicate_field");
                p.ws(); if (p.peek('}')) { p.take('}'); break; } p.take(','); p.ws();
            }
            p.ws(); if (p.i != text.length()) throw new BadRequest("invalid_json");
            return out;
        }
        private String string() throws BadRequest {
            take('"'); StringBuilder b = new StringBuilder();
            while (i < text.length() && text.charAt(i) != '"') {
                char c = text.charAt(i++); if (c < 0x20 || c == '\\') throw new BadRequest("invalid_json_string"); b.append(c);
            }
            take('"'); return b.toString();
        }
        private String number() throws BadRequest {
            int start = i; if (peek('-')) i++;
            while (i < text.length() && Character.isDigit(text.charAt(i))) i++;
            if (start == i || (i == start + 1 && text.charAt(start) == '-')) throw new BadRequest("invalid_number");
            return text.substring(start, i);
        }
        private void ws() { while (i < text.length() && Character.isWhitespace(text.charAt(i))) i++; }
        private boolean peek(char c) { return i < text.length() && text.charAt(i) == c; }
        private void take(char c) throws BadRequest { if (!peek(c)) throw new BadRequest("invalid_json"); i++; }
    }

    private static final class BadRequest extends Exception { BadRequest(String m) { super(m); } }
    private static final class Conflict extends Exception { Conflict(String m) { super(m); } }
    private static final class LedgerCorruption extends Exception {}
    private static final class DecisionFailure extends Exception {}
}









