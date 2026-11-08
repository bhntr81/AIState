import json, tempfile, unittest
from pathlib import Path
import tally
class T(unittest.TestCase):
    def test_counts(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d); (d/"p").mkdir(); (d/"v").mkdir(); (d/"p/PROPOSAL_01_X.md").write_text("x")
            w = lambda n, o: (d/"v"/n).write_text(o if isinstance(o, str) else json.dumps(o))
            w("a.json", {"seat":1,"proposal":"PROPOSAL_01_X.md","support":True})
            w("b.json", {"seat":2,"proposal":"PROPOSAL_01_X.md","support":False})
            w("c.json", {"seat":3,"proposal":"PROPOSAL_01_X.md","support":"yes"})
            w("d.json", {"seat":1,"proposal":"PROPOSAL_01_X.md","support":True})
            w("e.json", {"seat":4,"ranking":["seat1"]})
            r = tally.tally(d/"v", d/"p")[0]
            self.assertEqual((r["yes"], r["no"], r["missing"]), ([1],[2],[3,4,5]))
            self.assertEqual(len(r["malformed"]), 2)
if __name__ == "__main__": unittest.main()
