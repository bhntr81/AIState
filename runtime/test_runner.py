import importlib, json, os, shutil, sys, tempfile, unittest
from pathlib import Path
SRC = Path(__file__).resolve().parent.parent
class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); (self.tmp/"runtime").mkdir()
        shutil.copytree(SRC/"founders", self.tmp/"founders", ignore=shutil.ignore_patterns(".git"))
        os.environ.update(AISTATE_ROOT=str(self.tmp), NO_FINALIZE="1", SEAT_MODEL_1="fake", SEAT_MODEL_2="fake", DAILY_CAP_USD="10", SEAT_DAILY_USD="2", MAX_WAKES_PER_SEAT="4")
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
    def test_precheck_skips_when_nothing_open_and_wakes_for_open_items(self):
        votes = self.tmp/"founders"/"votes"; props = self.tmp/"founders"/"proposals"
        for pf in props.glob("PROPOSAL_*.md"):                                    # make every proposal voted by seat 1 except none
            if pf.name.startswith("PROPOSAL_08_"): continue
            f = votes/f"{pf.stem}.seat1.json"
            if not f.exists(): f.write_text('{"seat":1,"proposal":"%s.md","support":true}' % pf.stem)
        for a in props.glob("SESSION_*.md"): (self.tmp/"founders"/"memory"/"seat1.state.json").write_text(json.dumps({f"proposals/{a.name}": __import__("hashlib").sha256(a.read_bytes()).hexdigest()[:12] for a in props.glob("SESSION_*.md")}))
        # clear unrelated open rounds/assignments for the test by checking only categories we control
        reasons = [r for r in self.r.open_items(1) if r.startswith("unvoted:")]
        self.assertEqual(reasons, [])                                              # nothing unvoted
        newp = props/"PROPOSAL_97_TEST.md"; newp.write_text("# test proposal")
        self.assertIn("unvoted:PROPOSAL_97_TEST.md", self.r.open_items(1))         # an unvoted proposal is an open item
        held = props/"PROPOSAL_08_TEST_HELD.md"; held.write_text("# held"); self.assertNotIn("unvoted:PROPOSAL_08_TEST_HELD.md", self.r.open_items(1))   # held plans are excluded
        (props/"SESSION_97_AGENDA.md").write_text("# a\n- **Seat 1:** draft `PROPOSAL_96_ASSIGNED.md`.\n")
        r2 = self.r.open_items(1); self.assertIn("new-agenda:SESSION_97_AGENDA.md", r2); self.assertIn("assigned-draft:PROPOSAL_96_ASSIGNED.md", r2)
    def test_secret_scan_blocks_keys_and_private_paths_but_not_normal_text(self):
        bad = ["+AIzaSyA1234567890abcdefghijklmnopqrstuvw", "+see /home/someone/API-KEYS/gemini", "+-----BEGIN PRIVATE KEY-----", "+file dao/keys/mainnet-seats.json"]
        for b in bad: self.assertTrue(self.r.scan_for_secrets(b), b)
        ok = "+Seat 3 votes YES on Proposal 22; the plan names no keys or paths.\n+tx hash 0x" + "ab" * 32 + "\n--- a/removed /home/kali/x"
        self.assertEqual(self.r.scan_for_secrets(ok), [])                       # prose, hashes and removed lines are fine
    def test_open_item_wakes_a_seat_even_when_files_unchanged(self):
        props = self.tmp/"founders"/"proposals"; os.environ["SEAT_MODEL_1"] = "fake"; os.environ["MIN_WAKE_INTERVAL_S"] = "0"
        new, now, st = self.r.new_work(1); st.write_text(json.dumps(now))             # state says: nothing new since last wake
        self.r.open_items = lambda seat: []                                             # nothing open -> asleep
        self.assertEqual(self.r.wake(1)["status"], "asleep")
        self.r.open_items = lambda seat: ["option-missing:NEXTSTEP9"]                   # something open, files unchanged -> wakes
        self.assertEqual(self.r.wake(1)["status"], "ran")
if __name__ == "__main__": unittest.main(verbosity=2)
