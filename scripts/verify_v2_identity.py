"""Audit the V2 definition; synthetic inputs are not material measurements.

Run from the repository root:
    python scripts/verify_v2_identity.py --output results/v2_identity_2026-11-08.json

Brent evaluates the two original integrals with adaptive quadrature. The
comparison uses NumPy's trapezoid rule, exact for the declared piecewise-linear
curve. Neither path invokes the historical threshold algorithm in arbe_lambda.py.
This audit is not a replacement production implementation or an empirical study.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq

A, B = 380.0, 730.0
WIDTH = B - A
SEED = 20261108
XTOL_NM = 1e-10
RTOL = 1e-14
CHECK_ATOL_NM = 1e-8


def validate(wavelengths, reflectances):
    w = np.asarray(wavelengths, dtype=float)
    r = np.asarray(reflectances, dtype=float)
    if w.ndim != 1 or r.ndim != 1 or len(w) != len(r) or len(w) < 2:
        raise ValueError("Expected equal one-dimensional arrays with at least two points")
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(r)):
        raise ValueError("All values must be finite")
    if np.any(np.diff(w) <= 0):
        raise ValueError("Wavelengths must be strictly increasing")
    if w[0] != A or w[-1] != B:
        raise ValueError("Input must cover exactly 380 through 730 nm; no extrapolation")
    if np.any(r < 0) or np.any(r > 1):
        raise ValueError("Reflectance must be in [0, 1]; convert percentages explicitly")
    return w, r


def _integral(w, r, lo, hi, complement=False):
    if lo == hi:
        return 0.0
    points = w[(w > lo) & (w < hi)]

    def integrand(x):
        value = float(np.interp(x, w, r))
        return 1.0 - value if complement else value

    return quad(integrand, lo, hi, points=points, limit=len(points) + 50,
                epsabs=1e-9, epsrel=1e-12)[0]


def balance(x, wavelengths, reflectances):
    w, r = validate(wavelengths, reflectances)
    if not A <= x <= B:
        raise ValueError("The balance position must be inside the domain")
    # Keep the original two integrals explicit; do not substitute A + area.
    return _integral(w, r, A, x, complement=True) - _integral(w, r, x, B)


def v2_brent(wavelengths, reflectances):
    w, r = validate(wavelengths, reflectances)
    return float(brentq(lambda x: balance(x, w, r), A, B,
                        xtol=XTOL_NM, rtol=RTOL))


def classical_fields(wavelengths, reflectances):
    """Integrate the same PL model; undefined normalized moments return None."""
    w, r = validate(wavelengths, reflectances)
    area = float(np.trapezoid(r, w))
    mean = area / WIDTH
    result = {"mean_reflectance": mean, "area_nm": area,
              "lambda_v2_direct_nm": A + area}
    if area == 0:
        result.update({k: None for k in ("lambda_ee_nm", "delta_lambda_nm",
                      "mu2_nm2", "sigma_star_nm", "mu3_nm3", "skewness_gamma1")})
        return result
    # Three-point Gauss-Legendre integrates degree <=5 exactly on each segment.
    # Work in t=(lambda-A)/WIDTH to avoid subtracting large raw moments.
    nodes, weights = np.polynomial.legendre.leggauss(3)
    t = (w - A) / WIDTH
    half = np.diff(t) / 2
    mid = (t[:-1] + t[1:]) / 2
    q = mid[:, None] + half[:, None] * nodes
    rq = r[:-1, None] + (r[1:] - r[:-1])[:, None] * (nodes + 1) / 2
    masses = half[:, None] * weights * rq
    c = float(np.sum(q * masses) / mean)
    mu2 = float(np.sum((q - c) ** 2 * masses) / mean * WIDTH ** 2)
    mu3 = float(np.sum((q - c) ** 3 * masses) / mean * WIDTH ** 3)
    ee = A + WIDTH * c
    result.update(lambda_ee_nm=ee, delta_lambda_nm=A + area - ee,
                  mu2_nm2=mu2, sigma_star_nm=float(np.sqrt(mu2)),
                  mu3_nm3=mu3,
                  skewness_gamma1=mu3 / mu2 ** 1.5 if mu2 > 0 else None)
    return result


def audit_cases():
    """Fixed, fully reconstructible suite; no source/master data are loaded."""
    rng = np.random.default_rng(SEED)
    grids = {
        "1nm": np.linspace(A, B, 351),
        "5nm": np.linspace(A, B, 71),
        "10nm": np.linspace(A, B, 36),
        "irregular": np.r_[A, np.sort(rng.uniform(A, B, 34)), B],
    }
    for name, w in grids.items():
        t = (w - A) / WIDTH
        for level in (0.0, 0.2, 0.3, 0.5, 1.0):
            yield "constant", f"{name}/constant/{level}", w, np.full_like(w, level)
        yield "ramp", name + "/rising", w, t
        yield "ramp", name + "/falling", w, 1 - t
        yield "oscillation", name + "/oscillation", w, 0.5 + 0.4 * np.cos(8*np.pi*t)
        for i in range(96):
            yield "random", f"{name}/random/{i}", w, rng.uniform(0, 1, len(w))
        base = 0.25 + 0.5 * t
        for i in range(32):
            # Bounded additive perturbations: no clipping changes the input model.
            yield "perturbed", f"{name}/perturbed/{i}", w, base + rng.uniform(-0.05, 0.05, len(w))


def run_audit():
    counts, errors, residuals = Counter(), [], []
    worst = None
    for group, name, w, r in audit_cases():
        direct = classical_fields(w, r)["lambda_v2_direct_nm"]
        brent = v2_brent(w, r)
        error = abs(brent - direct)
        residual = abs(balance(direct, w, r))
        if error > CHECK_ATOL_NM or residual > CHECK_ATOL_NM:
            raise AssertionError((name, error, residual))
        if not errors or error > max(errors):
            worst = name
        counts[group] += 1
        errors.append(error)
        residuals.append(residual)

    examples = {}
    for name, w, r in [
        ("constant_20_percent", [A, B], [0.2, 0.2]),
        ("constant_30_percent", [A, B], [0.3, 0.3]),
        ("linear_12_to_48_percent", [A, B], [0.12, 0.48]),
        ("triangle", [A, 555, B], [0, 1, 0]),
    ]:
        examples[name] = classical_fields(w, r)
        examples[name]["lambda_v2_brent_nm"] = v2_brent(w, r)

    code_path = Path(__file__)
    return {
        "status": "PASS",
        "scope": "Synthetic numerical verification of the stated mathematical identity; not empirical validation or novelty proof",
        "source_definition_commit": "cb566dddca3adeecbd8ac3b8ac352d270d7df585",
        "sign_convention": "delta_lambda_nm = lambda_v2_nm - lambda_ee_nm",
        "domain_nm": [A, B], "curve_model": "piecewise linear",
        "seed": SEED, "cases": len(errors), "case_groups": dict(counts),
        "max_brent_minus_direct_abs_nm": max(errors),
        "max_original_balance_residual_abs_nm": max(residuals),
        "worst_case": worst,
        "brent_xtol_nm": XTOL_NM, "brent_rtol": RTOL,
        "comparison_atol_nm": CHECK_ATOL_NM,
        "quadrature_epsabs_nm": 1e-9, "quadrature_epsrel": 1e-12,
        "python": platform.python_version(), "numpy": np.__version__,
        "scipy": scipy.__version__,
        "script_sha256": hashlib.sha256(code_path.read_bytes()).hexdigest(),
        "examples": examples,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_audit()
    text = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
