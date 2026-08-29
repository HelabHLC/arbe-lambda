#!/usr/bin/env python3
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

FILES=(Path("SIMULATION_PROTOCOL_V0_2.md"),Path("simulation_plan_v0_2.json"),Path("SIMULATION_PROTOCOL_V0_2_CHANGELOG.md"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    plan=json.loads(FILES[1].read_text())
    assert plan["global_boundary_effect"] not in plan["global_power_effects"]
    assert plan["topology_boundary_effect"] not in plan["topology_power_effects"]
    assert min(plan["global_power_effects"])>plan["global_boundary_effect"]
    assert min(plan["topology_power_effects"])>plan["topology_boundary_effect"]
    assert sum(plan["partition_fraction"].values())==1.0
    assert plan["study_a_empirical_thresholds_changed"] is False
    assert plan["simulation_restart_authorised"] is False
    assert plan["empirical_confirmatory_run_authorised"] is False
    files={str(p):sha(p) for p in FILES}
    aggregate=hashlib.sha256("\n".join(f"{k}:{files[k]}" for k in sorted(files)).encode()).hexdigest()
    lock={"schema":"atlas_arbe_simulation_protocol_lock_v0_2","created_utc":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
          "status":"LOCKED_RESTART_NOT_YET_AUTHORISED","files":files,"aggregate_sha256":aggregate,
          "simulation_restart_authorised":False,"empirical_confirmatory_run_authorised":False}
    Path("SIMULATION_PROTOCOL_V0_2_LOCK.json").write_text(json.dumps(lock,indent=2)+"\n")
    print(json.dumps(lock,indent=2))
if __name__=="__main__": main()
