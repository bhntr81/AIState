import importlib, json, os, shutil, sys, tempfile, unittest
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent
class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); (self.tmp/"runtime").mkdir()
        shutil.copytree(SRC/"founders", self.tmp/"founders", ignore=shutil.ignore_patterns(".git"))
        os.environ.update(AISTATE_ROOT=str(self.tmp), NO_FINALIZE="1", SEAT_MODEL_1="fake", SEAT_MODEL_2="fake", DAILY_CAP_USD="10")
        os.environ.pop("MIN_WAKE_INTERVAL_S", None)
        sys.path.insert(0, str(SRC/"runtime"))
        if "runner" in sys.modules: del sys.modules["runner"]
        self.r = importlib.import_module("runner")
    def tearDown(self): shutil.rmtree(self.tmp, ignore_errors=True)
    def test_pause_halts(self):
        (self.tmp/"runtime"/"PAUSE").write_text("stop")
        out = self.r.wake(1, supervised=True)
        self.assertEqual(out["status"], "halted"); self.assertIn("paused", out["reason"])
        self.assertFalse((self.tmp/"founders"/"votes"/"TESTVOTE.seat1.json").exists())      # the model never ran
    def test_budget_cap_halts(self):
        (self.tmp/"runtime"/f"spend-{__import__('datetime').date.today()}.txt").write_text("9.995")
        out = self.r.wake(1, supervised=True)
        self.assertEqual(out["status"], "halted"); self.assertIn("cap", out["reason"])
    def test_seat_budget_and_wake_limit(self):
        for _ in range(self.r.MAX_WAKES): self.r.record_cost(1, 0.01, "fake")
        out = self.r.wake(1, supervised=True); self.assertEqual(out["status"], "halted"); self.assertIn("wakes", out["reason"])
    def test_tampered_identity_refused(self):
        p = self.tmp/"founders"/"identity"/"seat1.identity.json"; d = json.loads(p.read_text()); d["name"] = "evil"; p.write_text(json.dumps(d, indent=2))
        out = self.r.wake(1, supervised=True); self.assertEqual(out["status"], "refused")
    def test_untampered_identity_passes_and_path_writes_reverted(self):
        before_rules = (self.tmp/"founders"/"CONVENTION_RULES.md").read_bytes(); before_id = (self.tmp/"founders"/"identity"/"seat1.identity.json").read_bytes()
        before_mem2 = (self.tmp/"founders"/"memory"/"seat2.md").read_bytes()
        out = self.r.wake(1, supervised=True)
        self.assertEqual(out["status"], "ran", out)
        self.assertTrue((self.tmp/"founders"/"votes"/"TESTVOTE.seat1.json").exists())            # own vote file allowed
        self.assertEqual((self.tmp/"founders"/"CONVENTION_RULES.md").read_bytes(), before_rules) # reverted
        self.assertEqual((self.tmp/"founders"/"identity"/"seat1.identity.json").read_bytes(), before_id)
        self.assertEqual((self.tmp/"founders"/"memory"/"seat2.md").read_bytes(), before_mem2)    # other seat's memory untouched
        self.assertGreaterEqual(len(out["reverted_writes"]), 3)
    def test_no_new_work_sleeps(self):
        self.r.wake(1, supervised=True); (self.tmp/"runtime"/"runner.lock").unlink(missing_ok=True)
        out = self.r.wake(2); self.assertIn(out["status"], ("asleep", "halted", "ran"))        # unsupervised respects interval/work checks
        out1 = self.r.wake(1); self.assertEqual(out1["status"], "halted")                      # min interval not elapsed
    def test_runner_state_idle_running_stale(self):
        import fcntl, subprocess
        self.assertEqual(self.r.runner_state(), ("idle", None))                       # no lock file yet
        lock = self.tmp/"runtime"/"runner.lock"
        holder = open(lock, "a+"); fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB); holder.seek(0); holder.truncate(); holder.write(str(os.getpid())); holder.flush()
        state, pid = self.r.runner_state(); self.assertEqual((state, pid), ("running", os.getpid()))   # a live holder
        fcntl.flock(holder, fcntl.LOCK_UN); holder.close()
        dead = subprocess.Popen(["true"]); dead.wait(); lock.write_text(str(dead.pid))                    # file names a dead process
        self.assertEqual(self.r.runner_state(), ("stale", dead.pid))
        lock.write_text(""); self.assertEqual(self.r.runner_state(), ("idle", None))                    # cleaned up
    def test_state_check_ignores_command_lines(self):
        import subprocess
        p = subprocess.Popen(["sleep", "3", "runtime/runner.py", "cycle"])                            # a process whose command line LOOKS like a cycle
        try: self.assertEqual(self.r.runner_state(), ("idle", None))
        finally: p.kill()
if __name__ == "__main__": unittest.main(verbosity=2)
