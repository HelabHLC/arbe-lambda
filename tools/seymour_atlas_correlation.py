#!/usr/bin/env python3
"""Reproduce the Seymour correlation test for the 13,283 ATLAS HLC spectra.

Input: trusted local ATLAS master pickle containing one row per reference and
       R_380, R_390, ..., R_730 columns (reflectance as fractions from 0 to 1).
Output: full per-reference CSV, scatterplot PNG, and console statistics.

SECURITY: pandas pickle input can execute code; load only your trusted master.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WAVELENGTHS = np.arange(380, 731, 10, dtype=float)
COLUMNS = [f"R_{int(nm)}" for nm in WAVELENGTHS]

def calculate(frame: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in ("reference", *COLUMNS) if c not in frame]
    if missing:
        raise ValueError(f"Missing input columns: {missing}")
    spectrum = frame[COLUMNS].to_numpy(dtype=float)
    if not np.isfinite(spectrum).all() or np.any((spectrum < 0) | (spectrum > 1)):
        raise ValueError("Reflectance must be finite and between 0 and 1")
    area = np.trapezoid(spectrum, WAVELENGTHS, axis=1)
    if np.any(area <= 0):
        raise ValueError("Zero-integral spectrum: centroid is undefined")
    mean = area / (WAVELENGTHS[-1] - WAVELENGTHS[0])
    lambda_v2 = WAVELENGTHS[0] + area
    lambda_ee = np.trapezoid(spectrum * WAVELENGTHS, WAVELENGTHS, axis=1) / area
    delta = lambda_v2 - lambda_ee
    rowids = frame["atlas_row_id"].to_numpy() if "atlas_row_id" in frame else np.arange(len(frame))
    return pd.DataFrame({
        "atlas_row_id": rowids,
        "reference": frame["reference"].to_numpy(),
        "mean_reflectance": mean,
        "lambda_v2_nm": lambda_v2,
        "lambda_ee_nm": lambda_ee,
        "delta_lambda_nm": delta,
    })

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("master", type=Path, help="Trusted ATLAS master .pkl")
    p.add_argument("--out", type=Path, default=Path("results/seymour-atlas"))
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    frame = pd.read_pickle(args.master)
    result = calculate(frame)
    if len(result) != 13283:
        raise ValueError(f"Expected 13,283 references; received {len(result)}")
    if result["reference"].duplicated().any():
        raise ValueError("Duplicate reference identifiers")
    csv_path = args.out / "ARBE_Seymour_ATLAS_13283_Einzelwerte.csv"
    png_path = args.out / "ARBE_Seymour_ATLAS_13283_Streudiagramm.png"
    result.to_csv(csv_path, index=False, float_format="%.12f")
    x = result["mean_reflectance"].to_numpy()
    y = result["delta_lambda_nm"].to_numpy()
    pearson = float(np.corrcoef(x, y)[0, 1])
    spearman = float(np.corrcoef(result["mean_reflectance"].rank().to_numpy(), result["delta_lambda_nm"].rank().to_numpy())[0, 1])
    slope, intercept = np.polyfit(x, y, 1)
    xline = np.linspace(x.min(), x.max(), 200)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(x, y, s=5, alpha=0.28, rasterized=True)
    ax.plot(xline, slope*xline + intercept, linewidth=2, label="Linear regression")
    ax.set(xlabel="Mean spectral reflectance (0–1)", ylabel="ARBE Δλ* (nm)",
           title="13,283 ATLAS reference spectra — Seymour correlation test")
    ax.text(0.02, 0.98, f"N = {len(result):,}\nPearson r = {pearson:.4f}\nR² = {pearson**2:.4f}\nSpearman ρ = {spearman:.4f}",
            transform=ax.transAxes, ha="left", va="top")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.22)
    fig.tight_layout()
    fig.savefig(png_path, dpi=180)
    plt.close(fig)
    print(f"N={len(result)}; Pearson r={pearson:.10f}; R²={pearson**2:.10f}; Spearman rho={spearman:.10f}")
    print(f"CSV: {csv_path}\nPNG: {png_path}")

if __name__ == "__main__":
    main()
