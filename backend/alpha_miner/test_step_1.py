import os
import unittest

from alpha_algorithm import AlphaAlgorithm

# Sample logs ship with the repo in backend/static/uploads.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads')

class TestStep1(unittest.TestCase):

    def test_L1(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L1.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(observed,expected)

    def test_L2(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L2.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e', 'f']
        self.assertEqual(observed,expected)

    def test_L3(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L3.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.assertEqual(observed,expected)

    def test_L4(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L4.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(observed,expected)

    def test_L5(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L5.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e', 'f']
        self.assertEqual(observed,expected)

    def test_L6(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L6.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.assertEqual(observed,expected)

    def test_L7(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'L7.xes'))
        observed = self.x.step_1()
        expected = ['a', 'b', 'c']
        self.assertEqual(observed,expected)

    def test_bill_instances(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'billinstances.xes'))
        observed = self.x.step_1()
        expected = ['deliver bill', 'print bill', 'write bill']
        self.assertEqual(observed,expected)

    def test_flyer_instances(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'flyerinstances.xes'))
        observed = self.x.step_1()
        expected = ['deliver flyer', 'design flyer', 'print flyer', 'receive flyer order', 'send draft to customer']
        self.assertEqual(observed,expected)

    def test_poster_instances(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'posterinstances.xes'))
        observed = self.x.step_1()
        expected = ['deliver poster', 'design photo poster', 'print poster', 'receive order and photo']
        self.assertEqual(observed,expected)

    def test_running_example(self):
        self.x = AlphaAlgorithm(os.path.join(DATA_DIR, 'running-example.xes'))
        observed = self.x.step_1()
        expected = ['check ticket', 'decide', 'examine casually', 'examine thoroughly', 'pay compensation', 'register request', 'reinitiate request', 'reject request']
        self.assertEqual(observed,expected)

if __name__ == '__main__':
    unittest.main()