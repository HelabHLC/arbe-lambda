"""ARBE Delta working calculator 0.1.0: fixed-grid reflectance analysis.

Research implementation, not instrument certification or a Brent-procedure claim.
Uncertainty is unknown unless supplied. No noise filtering or inferred calibration.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

VERSION = "0.1.0"
ORDER = ["area_nm", "centroid_nm", "lambda_v2_nm", "delta_lambda_nm"]


def integration_weights(wavelength_nm, integration="piecewise_linear"):
    """Area and first moment about the first wavelength, both linear in R.

    The piecewise_linear weights integrate lambda*R(lambda) exactly for
    a linear interpolant R. point_trapezoid reproduces the attached algorithm.
    """
    lam = np.asarray(wavelength_nm, dtype=float)
    if lam.ndim != 1 or lam.size < 2 or not np.all(np.isfinite(lam)):
        raise ValueError("At least two finite one-dimensional wavelengths required.")
    h = np.diff(lam)
    if np.any(h <= 0):
        raise ValueError("Wavelengths must be strictly increasing; no duplicates.")
    q = np.zeros(lam.size, dtype=float)
    q[:-1] += h / 2
    q[1:] += h / 2
    u = lam - lam[0]
    if integration == "piecewise_linear":
        t = np.zeros(lam.size, dtype=float)
        t[:-1] += h * (2 * u[:-1] + u[1:]) / 6
        t[1:] += h * (u[:-1] + 2 * u[1:]) / 6
    elif integration == "point_trapezoid":
        t = q * u
    else:
        raise ValueError("integration must be piecewise_linear or point_trapezoid.")
    return q, t


def calculate(wavelength_nm, reflectance, *, standard_uncertainty=None,
              reflectance_covariance=None, interval_nm=(380.0, 730.0),
              integration="piecewise_linear"):
    """Return A, c, V2, D and optional joint first-order uncertainty.

    All reflectances and their uncertainties use fractions, not percent.
    The covariance argument describes the same reflectance nodes as the data.
    Fixed, exact wavelength nodes are assumed; this is not a full instrument
    uncertainty budget. Invalid data are rejected, never silently clipped.
    """
    lam = np.asarray(wavelength_nm, dtype=float)
    r = np.asarray(reflectance, dtype=float)
    q, t = integration_weights(lam, integration)
    bounds = np.asarray(interval_nm, dtype=float)
    if bounds.shape != (2,) or not np.all(np.isfinite(bounds)) or bounds[0] >= bounds[1]:
        raise ValueError("interval_nm must specify two finite increasing bounds.")
    if lam[0] != bounds[0] or lam[-1] != bounds[1]:
        raise ValueError("Wavelength endpoints must match the declared fixed interval.")
    if r.shape != lam.shape or not np.all(np.isfinite(r)):
        raise ValueError("Reflectance must be a finite vector matching wavelengths.")
    if np.any((r < 0) | (r > 1)):
        raise ValueError("Reflectance must lie in [0,1]; percent input is not converted.")
    area = float(q @ r)
    if not np.isfinite(area) or area <= 0:
        raise ValueError("Positive finite area is required for centroid and D.")
    offset = float((t @ r) / area)
    centroid = float(lam[0] + offset)
    v2 = float(lam[0] + area)
    delta = float(area - offset)
    jc = (t - offset * q) / area
    jacobian = np.vstack([q, jc, q, q - jc])
    if not np.all(np.isfinite(jacobian)):
        raise ValueError("Non-finite sensitivity: area too small for this calculation.")

    if standard_uncertainty is not None and reflectance_covariance is not None:
        raise ValueError("Supply standard_uncertainty OR reflectance_covariance, not both.")
    covariance = None
    uncertainty_model = "not_provided"
    notes = []
    if standard_uncertainty is not None:
        u = np.asarray(standard_uncertainty, dtype=float)
        if u.ndim == 0:
            u = np.full(r.shape, float(u), dtype=float)
        if u.shape != r.shape or not np.all(np.isfinite(u)) or np.any(u < 0):
            raise ValueError("Standard uncertainties must be finite, nonnegative and match R.")
        covariance = np.diag(u ** 2)
        if not np.all(np.isfinite(covariance)):
            raise ValueError("Uncertainty covariance overflow.")
        uncertainty_model = "supplied_uncorrelated_reflectance_standard_uncertainties"
    elif reflectance_covariance is not None:
        covariance = np.asarray(reflectance_covariance, dtype=float)
        if covariance.shape != (r.size, r.size) or not np.all(np.isfinite(covariance)):
            raise ValueError("Covariance must be a finite n by n matrix.")
        scale = max(float(np.max(np.abs(covariance))), np.finfo(float).tiny)
        tol = 100 * np.finfo(float).eps * r.size * scale
        if np.max(np.abs(covariance - covariance.T)) > tol:
            raise ValueError("Covariance must be symmetric.")
        covariance = (covariance + covariance.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(covariance)
        if eigenvalues[0] < -tol:
            raise ValueError("Covariance must be positive semidefinite.")
        if eigenvalues[0] < 0:
            covariance = (eigenvectors * np.maximum(eigenvalues, 0)) @ eigenvectors.T
            notes.append("Tiny negative covariance eigenvalues within roundoff were set to zero.")
        uncertainty_model = "supplied_full_reflectance_covariance"

    output_covariance = None
    output_uncertainty = None
    if covariance is not None:
        output_covariance = jacobian @ covariance @ jacobian.T
        output_covariance = (output_covariance + output_covariance.T) / 2
        if not np.all(np.isfinite(output_covariance)):
            raise ValueError("Output covariance is not finite.")
        sd = np.sqrt(np.maximum(np.diag(output_covariance), 0))
        output_uncertainty = dict(zip(ORDER, map(float, sd)))
        if sd[0] / area >= 0.1:
            notes.append("u(A)/A >= 0.1: first-order propagation may be inadequate; validate with a physical distribution model. This threshold is only a diagnostic flag.")
        output_covariance = output_covariance.tolist()

    return {
        "calculator_version": VERSION,
        "status": "research_working_version_not_experimentally_validated",
        "integration": integration,
        "interval_nm": bounds.tolist(),
        "area_nm": area,
        "mean_reflectance": area / float(bounds[1] - bounds[0]),
        "centroid_nm": centroid,
        "lambda_v2_nm": v2,
        "delta_lambda_nm": delta,
        "sign_convention": "lambda_V2_minus_lambda_EE",
        "uncertainty_model": uncertainty_model,
        "standard_uncertainty_nm": output_uncertainty,
        "covariance_order": ORDER,
        "covariance_nm2": output_covariance,
        "jacobian_wrt_reflectance": jacobian.tolist(),
        "limitations": [
            "Uncertainty covers only supplied reflectance errors at fixed wavelength nodes.",
            "No assumed default uncertainty; null means unknown, not zero.",
            "No outlier suppression, significance decision, material diagnosis, or full-spectrum reconstruction.",
            "V2 is evaluated by the exact area identity, not a Brent-Dekker procedure.",
            "An exact interpolant integral does not remove sampling or instrument uncertainty.",
        ],
        "notes": notes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    result = calculate(**payload)
    rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        if args.output.resolve() == args.input_json.resolve():
            raise ValueError("Output must not overwrite the input file.")
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
