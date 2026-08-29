import unittest
from run_simulation_gate0 import calibrate, replicate, seed_for
import numpy as np

class Gate0Tests(unittest.TestCase):
    def test_seed_reproducible(self): self.assertEqual(seed_for(1,"S0_NULL",100,2),seed_for(1,"S0_NULL",100,2))
    def test_effect_calibration(self):
        rng=np.random.default_rng(1); s=rng.normal(size=10000); e=rng.normal(size=10000)
        a=calibrate(s,e,.10); gain=1-np.mean(abs(e))/np.mean(abs(e+a*s))
        self.assertAlmostEqual(gain,.10,places=3)
    def test_replicate_reproducible(self): self.assertEqual(replicate("S0_NULL",100,0),replicate("S0_NULL",100,0))
    def test_empirical_confirmation_stays_locked(self):
        import json
        from pathlib import Path
        a=json.loads(Path("SIMULATION_EXECUTION_AUTHORIZATION.json").read_text())
        self.assertFalse(a["empirical_confirmatory_run_authorised"])

if __name__=="__main__": unittest.main()
