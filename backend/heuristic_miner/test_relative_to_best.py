import os
import tempfile
import unittest

from heuristic_mining import HeuristicMiner

# UI defaults: dependency 0.9, AND 0.1, positive observations 3, relative to best 0.05
DEFAULTS = (0.9, 0.1, 3, 0.05)


def write_log(traces):
    """Write traces (lists of activity names) to a minimal XES file, return its path."""
    events = lambda t: "".join(f'<event><string key="concept:name" value="{a}"/></event>' for a in t)
    xes = "<log>" + "".join(f"<trace>{events(t)}</trace>" for t in traces) + "</log>"
    f = tempfile.NamedTemporaryFile("w", suffix=".xes", delete=False)
    f.write(xes)
    f.close()
    return f.name


def flatten(entries):
    """Activities in an input/output list, including those inside XOR tuples."""
    return [a for e in entries for a in (e if isinstance(e, tuple) else (e,))]


class TestRelativeToBest(unittest.TestCase):

    def mine(self, traces, params=DEFAULTS):
        path = write_log(traces)
        self.addCleanup(os.remove, path)
        miner = HeuristicMiner(path, *params)
        miner.step_1()
        miner.step_2()
        return miner

    def test_strong_dependency_is_kept(self):
        # a=>b is seen 100 times and never reversed: 100/101 = 0.99. It is the best
        # (strongest) dependency of a, so it must be accepted, not dropped for being
        # "too far above" the dependency threshold.
        miner = self.mine([["a", "b", "c"]] * 100)
        self.assertEqual(miner.dependency[("a", "b")], 0.99)
        self.assertEqual(miner.output["a"], ["b"])
        self.assertEqual(miner.input["b"], ["a"])

    def test_weaker_sibling_is_filtered_relative_to_best(self):
        # a=>b: 100/101 = 0.99, a=>c: 10/11 = 0.909. Both pass the 0.9 threshold, but
        # a=>c is 0.081 below a's best outgoing edge (> 0.05), so it is not one of a's
        # outputs. For c's inputs, a=>c IS the best incoming edge, so it is kept there.
        miner = self.mine([["a", "b", "d"]] * 100 + [["a", "c", "d"]] * 10)
        self.assertEqual(miner.output["a"], ["b"])
        self.assertEqual(miner.input["c"], ["a"])

    def test_length_two_loop_does_not_crash(self):
        # b,c,b,c is a length-two loop: its pairs are counted in loops_two, not in
        # frequency. A strong loop (dependency 40/41 = 0.976) must be accepted
        # instead of raising a KeyError on the frequency lookup.
        miner = self.mine([["a", "b", "c", "b", "c", "d"]] * 20)
        self.assertIn("c", flatten(miner.output["b"]))
        # After c it's a choice: back to b (loop) or on to d, stored as an XOR tuple.
        self.assertIn("b", flatten(miner.output["c"]))
        self.assertIn("d", flatten(miner.output["c"]))


if __name__ == "__main__":
    unittest.main()
