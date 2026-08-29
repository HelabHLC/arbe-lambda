#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

PROTOCOL = Path("SIMULATION_PROTOCOL_V0_1.md")
PLAN = Path("simulation_plan_v0_1.json")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert plan["scenarios"] == ["S0_NULL", "S1_GLOBAL", "S2_TOPOLOGY"]
    assert 0.0 in plan["global_effect_mae_reduction"]
    assert 0.0 in plan["topology_effect_mae_reduction"]
    assert plan["simulation_execution_authorised"] is False
    assert plan["empirical_confirmatory_run_authorised"] is False
    files = {str(PROTOCOL): sha(PROTOCOL), str(PLAN): sha(PLAN)}
    aggregate = hashlib.sha256("\n".join(f"{k}:{files[k]}" for k in sorted(files)).encode()).hexdigest()
    lock = {
        "schema": "atlas_arbe_simulation_protocol_lock_v0_1",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "LOCKED_SIMULATION_NOT_YET_RUN",
        "files": files,
        "aggregate_sha256": aggregate,
        "simulation_execution_authorised": False,
        "empirical_confirmatory_run_authorised": False
    }
    Path("SIMULATION_PROTOCOL_LOCK.json").write_text(json.dumps(lock, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(lock, indent=2))


if __name__ == "__main__":
    main()
