import csv
from pathlib import Path
import sys

import pytest

# Ensure the project root is on sys.path so that `arbe_lambda` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from arbe_lambda import compute_lambda_star


def load_example_spectra():
    data_path = Path(__file__).parent / "data" / "example_spectra.csv"
    with data_path.open() as f:
        reader = csv.DictReader(f)
        wavelengths = []
        spectra = {}
        for row in reader:
            wavelengths.append(float(row["wavelength"]))
            for key, value in row.items():
                if key == "wavelength":
                    continue
                spectra.setdefault(key, []).append(float(value))
    return wavelengths, spectra


def test_lambda_star_from_example_dataset():
    wavelengths, spectra = load_example_spectra()
    expected = {
        "sample1": pytest.approx(494.2809, abs=0.001),
        "sample2": pytest.approx(505.7107, abs=0.001),
    }
    for name, reflectances in spectra.items():
        result = compute_lambda_star(wavelengths, reflectances)
        assert result == expected[name]
