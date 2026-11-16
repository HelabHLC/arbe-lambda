"""Synthetic acceptance tests for the proposed longitudinal ARBE decision rule.

These test mathematical classification only, not experimental calibration or diagnosis.
"""
import unittest


def interval_changes(values):
    return [right - left for left, right in zip(values, values[1:])]


def classify(change_nm, epsilon_nm):
    if epsilon_nm < 0:
        raise ValueError("epsilon must be nonnegative")
    if change_nm > epsilon_nm:
        return 1
    if change_nm < -epsilon_nm:
        return -1
    return 0


def qualified_reversal(values, epsilons):
    changes = interval_changes(values)
    if len(changes) != len(epsilons):
        raise ValueError("one epsilon is required per interval")
    signs = [classify(d, e) for d, e in zip(changes, epsilons)]
    return any(a * b == -1 for a, b in zip(signs, signs[1:]))


class TestLongitudinalARBE(unittest.TestCase):
    def test_signed_change_and_reversal(self):
        self.assertEqual(interval_changes([10, 12, 9]), [2, -3])
        self.assertTrue(qualified_reversal([10, 12, 9], [1, 1]))

    def test_boundary_is_indeterminate(self):
        self.assertEqual(classify(2, 2), 0)
        self.assertFalse(qualified_reversal([10, 12, 9], [2, 1]))

    def test_zero_is_not_reversal(self):
        self.assertFalse(qualified_reversal([10, 10, 9], [0, 0]))

    def test_negative_epsilon_rejected(self):
        with self.assertRaises(ValueError):
            classify(1, -0.1)

    def test_interval_threshold_count(self):
        with self.assertRaises(ValueError):
            qualified_reversal([10, 12, 9], [1])


if __name__ == "__main__":
    unittest.main()
