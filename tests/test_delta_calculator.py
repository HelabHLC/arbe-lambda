import numpy as np
import pytest
from scipy.integrate import quad
from scripts.delta_lambda import calculate


def values(result):
    return np.array([result[key] for key in result["covariance_order"]])


def test_uniform_analytic():
    r = calculate([380, 420, 555, 730], [.2] * 4)
    assert values(r) == pytest.approx([70, 555, 450, -105])
    assert r["mean_reflectance"] == pytest.approx(.2)


def test_linear_ramp_exact_interpolant():
    r = calculate([380, 730], [0, 1])
    assert values(r) == pytest.approx([175, 380 + 700/3, 555, -175/3])


def test_distinguishes_point_quadrature():
    w = np.arange(380., 731., 10.)
    r = (w-380)/350
    point = calculate(w, r, integration="point_trapezoid")
    exact = calculate(w, r)
    assert point["centroid_nm"] - exact["centroid_nm"] == pytest.approx(2/21)


def test_unknown_uncertainty_remains_unknown():
    r = calculate([380, 730], [1, 1])
    assert r["standard_uncertainty_nm"] is None
    assert r["covariance_nm2"] is None


def test_integer_inputs_do_not_truncate_explicit_noise():
    r = calculate([380, 555, 730], [1, 1, 1], standard_uncertainty=.002)
    assert r["standard_uncertainty_nm"]["delta_lambda_nm"] > 0


def test_explicit_zero_uncertainty_is_distinct_from_unknown():
    r = calculate([380, 730], [.5, .5], standard_uncertainty=0.)
    assert r["standard_uncertainty_nm"]["delta_lambda_nm"] == 0.
    assert r["uncertainty_model"] != "not_provided"


@pytest.mark.parametrize("w,r,kwargs", [
    ([380], [.5], {}),
    ([730,380], [.5,.5], {}),
    ([380,380,730], [.5,.5,.5], {}),
    ([380,730], [0,0], {}),
    ([380,730], [.5], {}),
    ([380,730], [.5,np.nan], {}),
    ([380,np.inf], [.5,.5], {}),
    ([380,730], [50,50], {}),
    ([380,730], [-.01,.5], {}),
    ([400,700], [.5,.5], {}),
    ([380,730], [.5,.5], {"standard_uncertainty":-.01}),
    ([380,730], [.5,.5], {"standard_uncertainty":[.01]}),
    ([380,730], [.5,.5], {"standard_uncertainty":np.nan}),
    ([380,730], [.5,.5], {"reflectance_covariance":[[1,2],[0,1]]}),
    ([380,730], [.5,.5], {"reflectance_covariance":[[1,2],[2,1]]}),
    ([380,730], [.5,.5], {"reflectance_covariance":[[1]]}),
    ([380,730], [.5,.5], {"standard_uncertainty":.01,"reflectance_covariance":np.eye(2)}),
    ([380,730], [.5,.5], {"integration":"unknown"}),
])
def test_rejects_invalid_input(w, r, kwargs):
    with pytest.raises(ValueError):
        calculate(w, r, **kwargs)


def test_explicit_alternative_interval():
    r = calculate([400,700],[.5,.5],interval_nm=(400,700))
    assert r["delta_lambda_nm"] == pytest.approx(0)


@pytest.mark.parametrize("integration", ["piecewise_linear", "point_trapezoid"])
def test_jacobian_independent_finite_differences(integration):
    w = np.array([380,401,455,560,618,730.])
    r = np.array([.21,.3,.6,.42,.37,.55])
    result = calculate(w,r,integration=integration)
    jac = np.asarray(result["jacobian_wrt_reflectance"])
    eps = 1e-6
    for i in range(w.size):
        plus, minus = r.copy(), r.copy()
        plus[i] += eps
        minus[i] -= eps
        numerical = (values(calculate(w,plus,integration=integration)) - values(calculate(w,minus,integration=integration))) / (2*eps)
        np.testing.assert_allclose(numerical,jac[:,i],rtol=2e-7,atol=1e-7)


def test_independent_adaptive_integration():
    w = np.array([380,412,500,571,650,730.])
    r = np.array([.1,.7,.31,.61,.2,.45])
    result = calculate(w,r)
    area = quad(lambda z: np.interp(z,w,r),w[0],w[-1],points=w[1:-1],epsabs=1e-10)[0]
    moment = quad(lambda z: z*np.interp(z,w,r),w[0],w[-1],points=w[1:-1],epsabs=1e-8)[0]
    assert result["area_nm"] == pytest.approx(area,abs=1e-10)
    assert result["centroid_nm"] == pytest.approx(moment/area,abs=1e-10)


def test_interpolant_subdivision_changes_no_values():
    w = np.array([380,420,570,730.])
    r = np.array([.15,.6,.3,.75])
    refined = np.sort(np.r_[w,(w[:-1]+w[1:])/2])
    np.testing.assert_allclose(values(calculate(w,r)),values(calculate(refined,np.interp(refined,w,r))),rtol=1e-14,atol=1e-12)


def test_covariance_transformation_and_inverse():
    w = np.array([380,470,555,650,730.])
    r = np.array([.2,.35,.55,.4,.3])
    cov = np.diag(np.full(5,1e-6)) + 4e-7*np.ones((5,5))
    result = calculate(w,r,reflectance_covariance=cov)
    out = np.asarray(result["covariance_nm2"])
    transform = np.array([[1,0],[1,-1.]])
    z = out[np.ix_([0,1],[0,1])]
    m = out[np.ix_([0,3],[0,3])]
    np.testing.assert_allclose(m,transform@z@transform.T,rtol=1e-13,atol=1e-14)
    np.testing.assert_allclose(z,transform@m@transform.T,rtol=1e-13,atol=1e-14)
    assert result["centroid_nm"] == pytest.approx(380+result["area_nm"]-result["delta_lambda_nm"])


def test_amplitude_shift_compensation_resolved_by_pair():
    w = np.sort(np.unique([380,451,455,551,555,651,655,730.]))
    r0 = .8*np.maximum(0,1-np.abs(w-555)/100)
    r1 = .95*.8*np.maximum(0,1-np.abs(w-551)/100)
    baseline, changed = calculate(w,r0), calculate(w,r1)
    assert changed["delta_lambda_nm"] == pytest.approx(baseline["delta_lambda_nm"])
    k = changed["area_nm"]/baseline["area_nm"]
    s = changed["area_nm"]-baseline["area_nm"]-(changed["delta_lambda_nm"]-baseline["delta_lambda_nm"])
    assert k == pytest.approx(.95)
    assert s == pytest.approx(-4.)


def test_different_spectra_can_share_both_parameters():
    w = np.array([380,435,495,560,645,730.])
    baseline = np.full(w.size,.5)
    jac = np.asarray(calculate(w,baseline)["jacobian_wrt_reflectance"])[[0,1]]
    perturbation = np.linalg.svd(jac,full_matrices=True)[2][-1]
    altered = baseline + .1*perturbation/np.max(np.abs(perturbation))
    np.testing.assert_allclose(values(calculate(w,baseline)),values(calculate(w,altered)),rtol=1e-14,atol=1e-12)
    assert np.max(np.abs(altered-baseline)) > .09
