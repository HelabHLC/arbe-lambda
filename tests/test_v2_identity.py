"""Analytic oracles and counterexamples, separate from historical threshold tests."""
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.verify_v2_identity import A, B, WIDTH, balance, classical_fields, v2_brent


@pytest.mark.parametrize("level", [0, 0.2, 0.3, 0.5, 1])
def test_constants_and_boundary_roots(level):
    assert v2_brent([A, B], [level, level]) == pytest.approx(A + WIDTH*level, abs=1e-9)


def test_analytic_linear_oracle():
    # R(t)=0.12+0.36t: mean .3, centroid t=.6, independent closed forms.
    f = classical_fields([A, B], [0.12, 0.48])
    assert v2_brent([A, B], [0.12, 0.48]) == pytest.approx(485)
    assert f["lambda_ee_nm"] == pytest.approx(590)
    assert f["delta_lambda_nm"] == pytest.approx(-105)


def test_centroid_alone_cannot_determine_delta_and_converse():
    x = classical_fields([A, B], [0.2, 0.2])
    y = classical_fields([A, B], [0.3, 0.3])
    z = classical_fields([A, B], [0.12, 0.48])
    assert x["lambda_ee_nm"] == pytest.approx(y["lambda_ee_nm"])
    assert x["delta_lambda_nm"] == pytest.approx(-105)
    assert y["delta_lambda_nm"] == pytest.approx(-70)
    assert z["delta_lambda_nm"] == pytest.approx(x["delta_lambda_nm"])
    assert abs(z["lambda_ee_nm"] - x["lambda_ee_nm"]) > 30


def test_uniform_sample_average_is_not_the_integral_average():
    w, r = [A, 555, B], [0, 1, 0]
    f = classical_fields(w, r)
    assert f["mean_reflectance"] == pytest.approx(0.5)
    assert v2_brent(w, r) == pytest.approx(555)
    assert A + WIDTH*np.mean(r) == pytest.approx(496.6666666666667)
    # Nor must R(V2) equal the mean reflectance or the local 50% level.
    assert np.interp(v2_brent(w, r), w, r) == pytest.approx(1)


def test_irregular_grid_and_interpolation_invariance():
    w, r = [A, 381, 487, 612, B], [0.1, 0.9, 0.3, 0.7, 0.4]
    dense = np.unique(np.r_[w, np.linspace(A, B, 351)])
    dense_r = np.interp(dense, w, r)
    assert v2_brent(w, r) == pytest.approx(v2_brent(dense, dense_r), abs=1e-9)
    for name in classical_fields(w, r):
        assert classical_fields(w, r)[name] == pytest.approx(classical_fields(dense, dense_r)[name], rel=1e-10, abs=1e-8)


def test_balance_is_affine_even_for_oscillating_spectrum():
    w, r = [A, 410, 500, 620, B], [0.1, 0.9, 0.2, 0.8, 0.1]
    for x, y in [(A, B), (400, 413), (501, 695)]:
        assert balance(y, w, r) - balance(x, w, r) == pytest.approx(y-x, abs=1e-9)


def test_discontinuous_spectrum_also_has_unique_root():
    # R=.2 before 520 nm and .8 after: area=.2*140+.8*210=196 nm.
    def r(x):
        return 0.2 if x < 520 else 0.8
    def integral(f, lo, hi):
        return quad(f, lo, hi, points=[520] if lo < 520 < hi else None)[0]
    def g(x):
        return integral(lambda z: 1-r(z), A, x) - integral(r, x, B)
    assert brentq(g, A, B) == pytest.approx(576)


def test_delta_is_not_a_pure_asymmetry_measure():
    # The normalized density for either constant curve is the same symmetric uniform density.
    f = classical_fields([A, B], [0.2, 0.2])
    assert f["mu2_nm2"] == pytest.approx(WIDTH**2/12)
    assert f["mu3_nm3"] == pytest.approx(0, abs=1e-8)
    assert f["skewness_gamma1"] == pytest.approx(0, abs=1e-12)
    assert f["delta_lambda_nm"] == pytest.approx(-105)


def test_same_seven_fields_do_not_imply_same_curve():
    # Shifted Legendre polynomial P4 is orthogonal to all polynomials degree <=3.
    def r0(t):
        return 0.5
    def r1(t):
        x = 2*t-1
        return 0.5 + 0.2*(35*x**4 - 30*x*x + 3)/8
    for k in range(4):
        assert quad(lambda t: t**k*r0(t), 0, 1)[0] == pytest.approx(
            quad(lambda t: t**k*r1(t), 0, 1)[0], abs=1e-12)
    assert r1(0) - r0(0) == pytest.approx(0.2)


def test_weighted_balance_is_a_different_definition():
    # Normalized t in [0,1], E(t)=1+t and R(t)=.2+.6t.
    r = lambda t: 0.2+0.6*t
    e = lambda t: 1+t
    def g(t):
        return quad(lambda u: e(u)*(1-r(u)), 0, t)[0] - quad(lambda u: e(u)*r(u), t, 1)[0]
    weighted_root = brentq(g, 0, 1)
    assert weighted_root != pytest.approx(0.5, abs=0.01)


def test_zero_area_has_no_centroid_or_delta():
    f = classical_fields([A, B], [0, 0])
    assert f["lambda_v2_direct_nm"] == A
    assert f["lambda_ee_nm"] is None
    assert f["delta_lambda_nm"] is None


@pytest.mark.parametrize("w,r", [
    ([A, B], [20, 30]), ([A, B], [-0.1, 0.5]), ([A, B], [0.1, 1.01]),
    ([A, B], [0.1, float("nan")]), ([A, B], [0.1, float("inf")]),
    ([A, A, B], [0.1, 0.2, 0.3]), ([B, A], [0.1, 0.2]),
    ([400, B], [0.1, 0.2]), ([A, 700], [0.1, 0.2]),
    ([A, B], [0.1]), ([A], [0.1]), ([[A, B]], [[0.1, 0.2]]),
])
def test_invalid_inputs_fail_explicitly(w, r):
    with pytest.raises(ValueError):
        v2_brent(w, r)
