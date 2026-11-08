"""Reproducible synthetic checks, not a laboratory validation."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from delta_lambda import calculate, integration_weights


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    seed, trials = 20261108, 50000
    w = np.arange(380., 731., 10.)
    r = .2 + .4*(w-380)/350 + .02*np.sin((w-380)/350*2*np.pi)
    sigma_white, sigma_offset, sigma_gain = 1e-4, 5e-5, 2e-4
    covariance = (sigma_white**2*np.eye(w.size)
                  + sigma_offset**2*np.ones((w.size,w.size))
                  + sigma_gain**2*np.outer(r,r))
    nominal = calculate(w,r,reflectance_covariance=covariance)
    rng = np.random.default_rng(seed)
    samples = (r + rng.normal(0,sigma_white,(trials,w.size))
               + rng.normal(0,sigma_offset,(trials,1))
               + rng.normal(0,sigma_gain,(trials,1))*r)
    assert np.all((samples >= 0) & (samples <= 1))
    q,t = integration_weights(w)
    areas = samples@q
    centroids = w[0] + (samples@t)/areas
    results = np.column_stack([areas,centroids,w[0]+areas,w[0]+areas-centroids])
    empirical = np.cov(results,rowvar=False,ddof=1)
    predicted = np.asarray(nominal["covariance_nm2"])
    ratios = np.sqrt(np.diag(empirical)/np.diag(predicted))
    assert np.all(np.abs(ratios-1) < .03), ratios
    full_relative_error = float(np.linalg.norm(empirical-predicted)/np.linalg.norm(predicted))
    assert full_relative_error < .05

    demo_w = np.arange(380,731)
    demo_r = .8*np.exp(-((demo_w-550)/40)**2)
    demo_r[demo_w < 550] *= .7
    wrong_noise = np.full_like(demo_w,.002)
    assert np.all(wrong_noise == 0)
    corrected = calculate(demo_w,demo_r,standard_uncertainty=.002,integration="point_trapezoid")
    ramp = (w-380)/350
    ramp_point = calculate(w,ramp,integration="point_trapezoid")
    ramp_linear = calculate(w,ramp)
    report = {
        "date":"2026-11-08",
        "evidence_level":"synthetic_numerical_verification_not_laboratory_validation",
        "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
        "seed":seed,"monte_carlo_repetitions":trials,
        "noise_assumptions":{"white_absolute_sd":sigma_white,"shared_offset_sd":sigma_offset,"shared_fractional_gain_sd":sigma_gain},
        "covariance_order":nominal["covariance_order"],
        "first_order_standard_uncertainty_nm":np.sqrt(np.diag(predicted)).tolist(),
        "monte_carlo_standard_deviation_nm":np.sqrt(np.diag(empirical)).tolist(),
        "monte_carlo_to_first_order_sd_ratio":ratios.tolist(),
        "relative_covariance_frobenius_error":full_relative_error,
        "validation_tolerances":{"relative_standard_deviation":.03,"relative_covariance_frobenius_norm":.05},
        "original_attachment_integer_noise_bug_reproduced":True,
        "corrected_attachment_point_model_u_D_nm":corrected["standard_uncertainty_nm"]["delta_lambda_nm"],
        "linear_ramp_centroid_point_nm":ramp_point["centroid_nm"],
        "linear_ramp_centroid_exact_interpolant_nm":ramp_linear["centroid_nm"],
        "calculator_sha256":hashlib.sha256((root/"delta_lambda.py").read_bytes()).hexdigest(),
        "validation_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "laboratory_data_used":False,
    }
    args.output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
