# Purpose: test integration (tests/test_integration.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import hashlib
import json
import os
import socket
import subprocess, shutil
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN_SUFFIX = ".exe" if os.name == "nt" else ""

class HybridApiIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="hybrid-lab-")
        cls.ledger = Path(cls.temp.name) / "transactions.chain"
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            cls.port = sock.getsockname()[1]
        env = os.environ.copy()
        env.update({
            "PORT": str(cls.port), "HOST": "127.0.0.1",
            "LEDGER_PATH": str(cls.ledger),
            "RUST_ADAPTER": str(ROOT / "rust" / "target" / "release" / ("txn-adapter" + BIN_SUFFIX)),
            "COBOL_ENGINE": str(ROOT / "build" / ("txn-engine" + BIN_SUFFIX)),
        })
        if os.environ.get("COB_CONFIG_DIR"):
            env["COB_CONFIG_DIR"] = os.environ["COB_CONFIG_DIR"]
        if os.name == "nt" and not env.get("COB_CONFIG_DIR"):
            cobc = shutil.which("cobc")
            if cobc: env["COB_CONFIG_DIR"] = str(Path(cobc).resolve().parent.parent / "config")
        cls.server = subprocess.Popen(
            ["java", "-cp", str(ROOT / "build" / "java"), "org.hybridlab.Main"],
            cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        deadline = time.time() + 15
        while time.time() < deadline:
            if cls.server.poll() is not None:
                raise RuntimeError("Java service exited: " + (cls.server.stdout.read() or ""))
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{cls.port}/health", timeout=0.3).close()
                return
            except Exception:
                time.sleep(0.1)
        cls.server.kill()
        raise RuntimeError("Java service did not become ready")

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        try:
            cls.server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.server.kill()
        cls.server.stdout.close()
        cls.temp.cleanup()

    def setUp(self):
        self.ledger.write_text("", encoding="utf-8")

    def post(self, body):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/transactions",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as exc:
            with exc:
                return exc.code, json.loads(exc.read())

    @staticmethod
    def transaction(key, operation="CREDIT", amount=100):
        return {"account_id": "acct-test", "idempotency_key": key, "operation": operation, "amount_cents": amount}

    def test_credit_debit_and_idempotent_replay(self):
        status, first = self.post(self.transaction("credit-001", amount=10000))
        self.assertEqual((status, first["status"], first["balance_cents"]), (201, "POSTED", 10000))
        status, second = self.post(self.transaction("debit-002", "DEBIT", 2500))
        self.assertEqual((status, second["balance_cents"]), (201, 7500))
        status, replay = self.post(self.transaction("credit-001", amount=10000))
        self.assertEqual((status, replay["status"], replay["balance_cents"], replay["replayed"]), (200, "REPLAY", 10000, True))
        self.assertEqual(len(self.ledger.read_text(encoding="utf-8").splitlines()), 2)

    def test_insufficient_funds_and_idempotency_conflict(self):
        status, result = self.post(self.transaction("withdraw-1", "DEBIT", 1))
        self.assertEqual((status, result["status"], result["balance_cents"]), (422, "REJECTED_INSUFFICIENT_FUNDS", 0))
        self.post(self.transaction("credit-1", amount=500))
        self.assertEqual(self.post(self.transaction("credit-1", amount=501))[0], 409)
        self.assertEqual(len(self.ledger.read_text(encoding="utf-8").splitlines()), 1)

    def test_invalid_request_does_not_change_ledger(self):
        status, _ = self.post({"account_id": "bad/id", "idempotency_key": "k", "operation": "CREDIT", "amount_cents": 1})
        self.assertEqual(status, 400)
        self.assertEqual(self.ledger.read_text(encoding="utf-8"), "")

    def test_concurrent_requests_serialize_and_chain_is_verifiable(self):
        count = 32
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda i: self.post(self.transaction(f"parallel-{i}", amount=7)), range(count)))
        self.assertTrue(all(code == 201 and result["status"] == "POSTED" for code, result in results))
        lines = self.ledger.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), count)
        previous = "0" * 64
        balance = 0
        for line in lines:
            account, key, operation, amount, after, prev, digest = line.split("|")
            self.assertEqual(prev, previous)
            expected = hashlib.sha256((previous + "|" + "|".join([account,key,operation,amount,after])).encode()).hexdigest()
            self.assertEqual(digest, expected)
            balance = int(after)
            previous = digest
        self.assertEqual(balance, count * 7)

    def test_tampered_journal_is_rejected_without_append(self):
        self.post(self.transaction("integrity-1", amount=25))
        line = self.ledger.read_text(encoding="utf-8").strip()
        self.ledger.write_text(line.replace("|25|", "|26|", 1) + "\n", encoding="utf-8")
        status, body = self.post(self.transaction("integrity-2", amount=1))
        self.assertEqual((status, body["error"]), (503, "ledger_integrity_failure"))

if __name__ == "__main__":
    unittest.main(verbosity=2)




