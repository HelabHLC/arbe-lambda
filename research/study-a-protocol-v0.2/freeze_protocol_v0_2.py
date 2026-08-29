#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

FILES = (Path("PROTOCOL_V0_2.md"), Path("analysis_plan_v0_2.json"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path in FILES:
        if not path.is_file():
            raise SystemExit(f"missing lock input: {path}")
    plan = json.loads(FILES[1].read_text(encoding="utf-8"))
    if plan.get("confirmatory_run_authorised") is not False:
        raise SystemExit("lock candidate must not authorise the confirmatory run")
    hashes = {str(path): digest(path) for path in FILES}
    aggregate = hashlib.sha256("\n".join(f"{k}:{hashes[k]}" for k in sorted(hashes)).encode()).hexdigest()
    out = {
        "schema": "atlas_arbe_protocol_lock_v0_2",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "LOCKED_NO_CONFIRMATORY_RUN_AUTHORISED",
        "files": hashes,
        "aggregate_sha256": aggregate
    }
    Path("PROTOCOL_LOCK.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
