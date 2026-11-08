# Simulation Protocol v0.1 package

Status: `LOCKED_SIMULATION_NOT_YET_RUN`

This package specifies power and recovery simulation for the ATLAS Clarus ×
ARBE λ* Study A decision procedure. It is separate from empirical Pilot PR #9,
Protocol v0.2 and Reviewer Packet v0.2.

## Contents

- `SIMULATION_PROTOCOL_V0_1.md` — human-readable protocol
- `simulation_plan_v0_1.json` — machine-readable design
- `SIMULATION_PROTOCOL_LOCK.json` — joint protocol lock
- `validate_simulation_protocol.py` — lock generator and validation
- `test_simulation_protocol.py` — protocol invariants
- `SHA256SUMS.txt` — package integrity inventory

## Non-claim

Simulation evaluates the method's ability to recover known synthetic truth. It
does not estimate the real ARBE effect and is not empirical evidence.

Both simulation and empirical confirmation remain unauthorised until their
respective governance gates are satisfied.
