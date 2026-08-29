import json,unittest
from pathlib import Path
from run_simulation_gate0_v0_2 import replicate,seed_for

class Gate0V02Tests(unittest.TestCase):
    def test_seed_reproducibility(self): self.assertEqual(seed_for(1,"x",2),seed_for(1,"x",2))
    def test_partition_isolation_and_fraction(self):
        r=replicate("S0_NULL",100,1); self.assertEqual(r["partition_sizes"],[20,60,20])
    def test_recoverable_global_calibration(self):
        r=replicate("S1_GLOBAL",400,2); self.assertAlmostEqual(r["recoverable_H1"],.15,delta=.006)
    def test_recoverable_topology_calibration(self):
        r=replicate("S2_TOPOLOGY",400,3); self.assertAlmostEqual(r["recoverable_H3"],.05,delta=.006)
    def test_signal_nonleakage_target(self):
        r=replicate("S1_GLOBAL",400,4); self.assertEqual(r["a_topology"],0.)
    def test_empirical_run_locked(self):
        a=json.loads(Path("SIMULATION_V0_2_RESTART_AUTHORIZATION.json").read_text());self.assertFalse(a["empirical_confirmatory_run_authorised"])
if __name__=="__main__":unittest.main()
