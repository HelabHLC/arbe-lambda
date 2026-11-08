import unittest

import numpy as np

from study_a_pilot import delta_e_00, stable_fold, topology_features


class StudyAPilotTests(unittest.TestCase):
    def test_ciede2000_reference_pair(self):
        # Sharma, Wu & Dalal supplementary test pair 1.
        a = np.array([[50.0, 2.6772, -79.7751]])
        b = np.array([[50.0, 0.0, -82.7485]])
        self.assertAlmostEqual(float(delta_e_00(a, b)[0]), 2.0425, places=4)

    def test_topology_detects_one_sign_change(self):
        d = np.array([[-0.2, -0.1, 0.1, 0.2]])
        out = topology_features(d)
        self.assertEqual(int(out[0, 0]), 1)
        self.assertEqual(int(out[0, 1]), 0)

    def test_fold_assignment_is_deterministic(self):
        ref = "H340_L050_C075"
        self.assertEqual(stable_fold(ref), stable_fold(ref))
        self.assertIn(stable_fold(ref), range(5))


if __name__ == "__main__":
    unittest.main()
