import csv
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from scripts.delta_lambda_pipeline import process_spectral_series, write_results

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/delta_synthetic.csv"


def write_csv(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_example_analytic_oracles():
    constant, ramp = process_spectral_series(EXAMPLE)
    assert constant["area_nm"] == pytest.approx(70)
    assert constant["centroid_nm"] == pytest.approx(555)
    assert constant["delta_lambda_nm"] == pytest.approx(-105)
    assert ramp["area_nm"] == pytest.approx(105)
    assert ramp["centroid_nm"] == pytest.approx(590)
    assert ramp["delta_lambda_nm"] == pytest.approx(-105)


def test_cli_csv_and_json_keep_unknown_uncertainty(tmp_path):
    output = tmp_path / "results.csv"
    run = subprocess.run([sys.executable, str(ROOT/"scripts/delta_lambda_pipeline.py"), str(EXAMPLE), "--output", str(output)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert "unknown, not zero" in run.stdout
    with output.open() as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["u_delta_lambda_nm"] == ""
    details = json.loads(output.with_suffix(".json").read_text())
    assert details["results"][0]["covariance_nm2"] is None


def test_cli_explicit_uncertainty_and_covariance_export(tmp_path):
    output = tmp_path / "results.csv"
    run = subprocess.run([sys.executable, str(ROOT/"scripts/delta_lambda_pipeline.py"), str(EXAMPLE), "--u-reflectance", ".002", "--output", str(output)], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    with output.open() as handle:
        rows = list(csv.DictReader(handle))
    assert float(rows[0]["u_delta_lambda_nm"]) > 0
    details = json.loads(output.with_suffix(".json").read_text())["results"][0]
    assert float(rows[0]["covariance_area_delta_nm2"]) == pytest.approx(details["covariance_nm2"][0][3])


def test_percent_data_and_uncertainty_convert_together(tmp_path):
    fraction = write_csv(tmp_path/"fractions.csv", "wavelength_nm,test\n380,0.2\n730,0.4\n")
    percent = write_csv(tmp_path/"percent.csv", "wavelength_nm,test\n380,20\n730,40\n")
    a = process_spectral_series(fraction, standard_uncertainty=.002)[0]
    b = process_spectral_series(percent, standard_uncertainty=.2, reflectance_unit="percent")[0]
    assert a["delta_lambda_nm"] == pytest.approx(b["delta_lambda_nm"])
    np.testing.assert_allclose(a["covariance_nm2"], b["covariance_nm2"])


def test_semicolon_decimal_comma_and_bom(tmp_path):
    source = write_csv(tmp_path/"european.csv", "\ufeffwavelength_nm;test\n380;0,2\n730;0,4\n")
    result = process_spectral_series(source, delimiter=";", decimal=",")[0]
    assert result["area_nm"] == pytest.approx(105)


def test_per_node_uncertainty_csv(tmp_path):
    u = write_csv(tmp_path/"uncertainty.csv", "wavelength_nm,a\n380,0.001\n730,0.002\n")
    data = write_csv(tmp_path/"data.csv", "wavelength_nm,a\n380,0.2\n730,0.4\n")
    result = process_spectral_series(data, uncertainty_csv=u)[0]
    assert result["standard_uncertainty_nm"]["area_nm"] == pytest.approx(175*np.sqrt(.001**2+.002**2))


def test_full_correlated_covariance_and_percent_scaling(tmp_path):
    data = write_csv(tmp_path/"data.csv", "wavelength_nm,a\n380,20\n730,40\n")
    covariance = tmp_path/"covariance.json"
    covariance.write_text(json.dumps({"a":[[.04,.02],[.02,.04]]}))
    result = process_spectral_series(data, covariance_json=covariance, reflectance_unit="percent")[0]
    assert result["uncertainty_model"] == "supplied_full_reflectance_covariance"
    assert result["standard_uncertainty_nm"]["area_nm"] == pytest.approx(175*np.sqrt(.12)/100)


@pytest.mark.parametrize("text", [
    "", "wavelength_nm\n380\n730\n",
    "Wavelength,a\n380,0.2\n730,0.4\n",
    "wavelength_nm,a,a\n380,0.2,0.2\n730,0.4,0.4\n",
    "wavelength_nm,\n380,0.2\n730,0.4\n",
    "wavelength_nm,=SUM(1)\n380,0.2\n730,0.4\n",
    "wavelength_nm,a\n380,0.2\n730,\n",
    "wavelength_nm,a\n380,0.2\n730,nan\n",
    "wavelength_nm,a\n380,0.2\n730,0.4,0.5\n",
    "wavelength_nm,a\n380,0.2\n",
    "wavelength_nm,a\n730,0.2\n380,0.4\n",
    "wavelength_nm,a\n380,20\n730,40\n",
])
def test_bad_csv_fails_explicitly(tmp_path, text):
    with pytest.raises(ValueError):
        process_spectral_series(write_csv(tmp_path/"bad.csv", text))


def test_uncertainty_headers_and_grid_must_match(tmp_path):
    bad_u = write_csv(tmp_path/"u.csv", "wavelength_nm,wrong\n380,0.01\n730,0.01\n")
    with pytest.raises(ValueError, match="identical"):
        process_spectral_series(EXAMPLE, uncertainty_csv=bad_u)


def test_missing_covariance_id_rejected(tmp_path):
    covariance = tmp_path/"cov.json"
    covariance.write_text('{}')
    with pytest.raises(ValueError, match="every spectrum"):
        process_spectral_series(EXAMPLE, covariance_json=covariance)


def test_multiple_uncertainty_sources_rejected():
    with pytest.raises(ValueError, match="only one"):
        process_spectral_series(EXAMPLE, standard_uncertainty=.01, uncertainty_csv="unused.csv")


def test_protects_inputs_and_existing_results(tmp_path):
    data = write_csv(tmp_path/"data.csv", "wavelength_nm,a\n380,0.2\n730,0.4\n")
    results = process_spectral_series(data)
    with pytest.raises(ValueError, match="input"):
        write_results(results, data, input_paths=[data], overwrite=True)
    output = tmp_path/"result.csv"
    write_results(results, output)
    with pytest.raises(ValueError, match="already exists"):
        write_results(results, output)
    write_results(results, output, overwrite=True)


def test_invalid_later_spectrum_leaves_no_output(tmp_path):
    source = write_csv(tmp_path/"bad.csv", "wavelength_nm,valid,invalid\n380,0.2,0\n730,0.4,0\n")
    output = tmp_path/"result.csv"
    run = subprocess.run([sys.executable, str(ROOT/"scripts/delta_lambda_pipeline.py"), str(source), "--output", str(output)], capture_output=True, text=True)
    assert run.returncode != 0
    assert "invalid" in run.stderr
    assert not output.exists()
    assert not output.with_suffix(".json").exists()
