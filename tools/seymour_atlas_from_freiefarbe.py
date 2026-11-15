#!/usr/bin/env python3
"""Rebuild the Seymour 13,283-reference CSV and scatterplot from freieFarbe CxF.

Input is the independently distributed HLC Colour Atlas XL ZIP, verified by SHA-256.
This reproducible path avoids distributing our private/augmented master pickle.
"""
from __future__ import annotations
import argparse
import hashlib
import io
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

from seymour_atlas_correlation import calculate

ZIP_SHA256 = "49d0bc10aeb90ee4b6f30d20305dd919caa37eca94e81a80ebf8e23b36ed1bdd"
REF_RE = re.compile(r"H\d{3}_L\d{3}_C\d{3}", re.IGNORECASE)
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
EXPECTED_N = 13283
EXPECTED_PEARSON = 0.8572758849535563

def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()

def parse_cxf(data: bytes) -> pd.DataFrame:
    root = ET.fromstring(data)
    records: dict[str, list[float]] = {}
    for obj in root.iter():
        if local(obj.tag) != "object":
            continue
        name = next((v for k, v in obj.attrib.items() if k.lower() == "name"), "")
        match = REF_RE.search(name)
        if not match:
            continue
        ref = match.group(0).upper()
        candidates = [
            s for s in obj.iter()
            if ("reflectance" in local(s.tag) and "spectrum" in local(s.tag))
            or local(s.tag) in ("reflectancespectrum", "reflectionspectrum")
        ]
        for spec in candidates:
            text = " ".join(t for t in spec.itertext() if t and t.strip())
            nums = [float(x) for x in NUMBER_RE.findall(text)]
            if len(nums) != 36:
                continue
            arr = np.asarray(nums, dtype=float)
            if arr.max() > 1.0 and arr.max() <= 100.0:
                arr /= 100.0
            if not np.all(np.isfinite(arr)) or arr.min() < 0 or arr.max() > 1:
                continue
            if ref in records:
                if not np.allclose(records[ref], arr, atol=1e-12):
                    raise ValueError(f"Duplicate reference with different spectrum: {ref}")
            else:
                records[ref] = arr.tolist()
            break
    if len(records) != EXPECTED_N:
        raise ValueError(
            f"Parsed {len(records)} unique 36-value spectra, expected {EXPECTED_N}; "
            "check the source CxF format before publishing"
        )
    ordered = sorted(records)
    return pd.DataFrame({"reference": ordered, **{
        f"R_{nm}": [records[k][i] for k in ordered]
        for i, nm in enumerate(range(380, 731, 10))
    }})

def main() -> None:
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("zip_file", type=Path)
    a.add_argument("--out", type=Path, default=Path("results/seymour-atlas"))
    args = a.parse_args()
    data = args.zip_file.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    if actual_sha != ZIP_SHA256:
        raise ValueError(f"ZIP checksum mismatch: {actual_sha}")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        candidates = [x for x in z.namelist() if x.lower().endswith(".cxf") and "spectraldata" in x.lower()]
        if len(candidates) != 1:
            raise ValueError(f"Expected one SpectralData CxF, found {candidates}")
        frame = parse_cxf(z.read(candidates[0]))
    result = calculate(frame)
    x = result["mean_reflectance"].to_numpy()
    y = result["delta_lambda_nm"].to_numpy()
    pearson = float(np.corrcoef(x, y)[0, 1])
    rho = float(np.corrcoef(result["mean_reflectance"].rank().to_numpy(), result["delta_lambda_nm"].rank().to_numpy())[0, 1])
    if not np.isclose(pearson, EXPECTED_PEARSON, atol=0.0002):
        raise ValueError(
            f"Expected Pearson r near {EXPECTED_PEARSON:.9f}; got {pearson:.9f}. "
            "Source/selection mismatch; no output will be published."
        )
    args.out.mkdir(parents=True, exist_ok=True)
    csv_path = args.out / "ARBE_Seymour_ATLAS_13283_Einzelwerte.csv"
    png_path = args.out / "ARBE_Seymour_ATLAS_13283_Streudiagramm.png"
    result.to_csv(csv_path, index=False, float_format="%.12f")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(x, y, s=5, alpha=0.28, rasterized=True)
    slope, intercept = np.polyfit(x, y, 1)
    xv = np.linspace(float(x.min()), float(x.max()), 200)
    ax.plot(xv, slope * xv + intercept, linewidth=2, label="Linear regression")
    ax.set(xlabel="Mean spectral reflectance (0–1)", ylabel="ARBE Δλ* (nm)",
           title="13,283 ATLAS reference spectra — Seymour correlation test")
    ax.text(0.02, 0.98,
            f"N = {len(result):,}\nPearson r = {pearson:.4f}\nR² = {pearson**2:.4f}\nSpearman ρ = {rho:.4f}",
            transform=ax.transAxes, va="top", ha="left")
    ax.grid(alpha=0.22)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(png_path, dpi=180)
    plt.close(fig)
    print(f"N={len(result)}, Pearson r={pearson:.9f}, R²={pearson**2:.9f}, rho={rho:.9f}")
    print(csv_path)
    print(png_path)

if __name__ == "__main__":
    main()
