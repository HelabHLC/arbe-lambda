#!/usr/bin/env python3
"""Generate a lightweight JSON payload for the ARBE λ* grid atlas.

The dataset `data/arbe_lambda_full_export.csv` contains the complete HLC Atlas
spectral export with Lab, sRGB and λ* values.  The browser-based grid only needs
selected fields, so we condense the CSV into `docs/arbe_lambda_grid.json` with
pre-parsed H/L/C metadata and rounded values for quick loading.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "arbe_lambda_full_export.csv"
JSON_PATH = ROOT / "docs" / "arbe_lambda_grid.json"


def parse_sample(sample: str) -> tuple[int, int, int]:
    """Extract hue, lightness and chroma integers from `Hxxx_Lyyy_Czzz` names."""
    try:
        hue_part, light_part, chroma_part = sample.split("_")
        hue = int(hue_part[1:])
        lightness = int(light_part[1:])
        chroma = int(chroma_part[1:])
    except Exception as exc:  # pragma: no cover - defensive guard for malformed rows
        raise ValueError(f"Unexpected sample format: {sample!r}") from exc
    return hue, lightness, chroma


def build_payload() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            sample = row["Sample"].strip()
            hue, lightness, chroma = parse_sample(sample)
            lambda_star = float(row["λ*"])
            lstar = float(row["L*"])
            astar = float(row["a*"])
            bstar = float(row["b*"])
            hex_value = row["HEX"].strip().upper()
            r = round(float(row["sRGB_R"]) * 255)
            g = round(float(row["sRGB_G"]) * 255)
            b = round(float(row["sRGB_B"]) * 255)
            rows.append(
                {
                    "sample": sample,
                    "hue": hue,
                    "lightness_step": lightness,
                    "chroma_step": chroma,
                    "lambda_nm": round(lambda_star, 3),
                    "lab": [round(lstar, 4), round(astar, 4), round(bstar, 4)],
                    "rgb": [max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))],
                    "hex": hex_value,
                }
            )
    return rows


def main() -> None:
    data = build_payload()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    updated = datetime.fromtimestamp(CSV_PATH.stat().st_mtime, tz=timezone.utc).isoformat()
    payload = {
        "updated": updated,
        "source": "HLC Colour Atlas XL (CC-BY-ND 4.0)",
        "items": data,
    }
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(ROOT)} with {len(data)} colors.")


if __name__ == "__main__":
    main()
