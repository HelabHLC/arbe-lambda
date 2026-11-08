"""Evaluate a local wide-format CSV without writing Python code.

Research tool: reflectance uncertainty at fixed wavelengths, not a full
instrument uncertainty budget. No input data are uploaded by this script.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

if __package__:
    from .delta_lambda import calculate
else:
    from delta_lambda import calculate


def read_spectra_csv(path, *, delimiter=",", decimal="."):
    """Require wavelength_nm followed by unique spectrum IDs and finite values."""
    if len(delimiter) != 1 or delimiter in ("\n", "\r"):
        raise ValueError("The delimiter must be one non-newline character.")
    if decimal not in (".", ",") or decimal == delimiter:
        raise ValueError("Choose decimal '.' or ',' distinct from the delimiter.")
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        header = next(reader, None)
        if header is None:
            raise ValueError("Empty CSV file.")
        header = [item.strip() for item in header]
        if len(header) < 2 or header[0] != "wavelength_nm":
            raise ValueError("First header must be wavelength_nm, followed by spectrum IDs.")
        if any(not item for item in header) or len(set(header)) != len(header):
            raise ValueError("CSV headers must be nonempty and unique.")
        # IDs are later written to CSV. Reject formula-like IDs rather than
        # silently changing the identity or creating spreadsheet formulas.
        if any(item[0] in "=+-@" for item in header[1:]):
            raise ValueError("Spectrum IDs must not start with =, +, - or @.")
        rows = []
        for row in reader:
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) != len(header):
                raise ValueError(f"CSV line {reader.line_num}: wrong number of fields.")
            try:
                values = [float(cell.strip().replace(decimal, ".")) for cell in row]
            except ValueError as exc:
                raise ValueError(f"CSV line {reader.line_num}: missing or nonnumeric value.") from exc
            if not np.all(np.isfinite(values)):
                raise ValueError(f"CSV line {reader.line_num}: all values must be finite.")
            rows.append(values)
    if len(rows) < 2:
        raise ValueError("At least two wavelength rows are required.")
    values = np.asarray(rows, dtype=float)
    return values[:, 0], header[1:], values[:, 1:]


def process_spectral_series(path, *, standard_uncertainty=None,
                            uncertainty_csv=None, covariance_json=None,
                            reflectance_unit="fraction", delimiter=",", decimal=".",
                            interval_nm=(380., 730.), integration="piecewise_linear"):
    """Return all results, validating the complete series before any file write.

    Uncertainty values use the chosen input unit; covariance uses its square.
    Covariance JSON maps each spectrum ID to its n x n reflectance covariance.
    Cross-spectrum covariances are not inferred or represented by this interface.
    """
    provided = sum(item is not None for item in
                   (standard_uncertainty, uncertainty_csv, covariance_json))
    if provided > 1:
        raise ValueError("Choose only one uncertainty input method.")
    if reflectance_unit not in ("fraction", "percent"):
        raise ValueError("reflectance_unit must be fraction or percent.")
    scale = 100. if reflectance_unit == "percent" else 1.
    wavelength, names, spectra = read_spectra_csv(path, delimiter=delimiter, decimal=decimal)
    uncertainty_values = None
    covariance_values = None
    if uncertainty_csv is not None:
        uw, un, uncertainty_values = read_spectra_csv(uncertainty_csv, delimiter=delimiter, decimal=decimal)
        if un != names or not np.array_equal(uw, wavelength):
            raise ValueError("Uncertainty CSV must have identical spectrum IDs and wavelength rows.")
    if covariance_json is not None:
        covariance_values = json.loads(Path(covariance_json).read_text(encoding="utf-8"))
        if not isinstance(covariance_values, dict) or set(covariance_values) != set(names):
            raise ValueError("Covariance JSON must map every spectrum ID, with no extra IDs.")

    results = []
    for column, name in enumerate(names):
        uncertainty = None
        covariance = None
        if standard_uncertainty is not None:
            uncertainty = float(standard_uncertainty) / scale
        elif uncertainty_values is not None:
            uncertainty = uncertainty_values[:, column] / scale
        elif covariance_values is not None:
            covariance = np.asarray(covariance_values[name], dtype=float) / scale**2
        try:
            result = calculate(wavelength, spectra[:, column] / scale,
                               standard_uncertainty=uncertainty,
                               reflectance_covariance=covariance,
                               interval_nm=interval_nm, integration=integration)
        except ValueError as exc:
            raise ValueError(f"Spectrum {name}: {exc}") from exc
        result["spectrum_id"] = name
        result["input_reflectance_unit"] = reflectance_unit
        results.append(result)
    return results


CSV_FIELDS = ["spectrum_id", "area_nm", "mean_reflectance", "centroid_nm",
              "lambda_v2_nm", "delta_lambda_nm", "u_area_nm", "u_centroid_nm",
              "u_lambda_v2_nm", "u_delta_lambda_nm", "covariance_area_delta_nm2",
              "uncertainty_model", "integration", "interval_start_nm",
              "interval_end_nm", "input_reflectance_unit", "calculator_version"]


def write_results(results, output_csv, *, input_paths=(), overwrite=False):
    output = Path(output_csv)
    if output.suffix.lower() != ".csv":
        raise ValueError("Output filename must end in .csv.")
    details = output.with_suffix(".json")
    reserved = {Path(p).resolve() for p in input_paths if p is not None}
    for target in (output, details):
        if target.resolve() in reserved:
            raise ValueError("An output path would overwrite an input file.")
        if target.exists() and not overwrite:
            raise ValueError(f"Output already exists: {target}; choose another name or --overwrite.")
    # Serialize completely first: invalid/NaN results cannot leave a CSV behind.
    rendered = json.dumps({
        "status": "research_results_not_industrial_release_decisions",
        "uncertainty_scope": "supplied_reflectance_errors_at_fixed_wavelengths_only",
        "cross_spectrum_covariance": "not_evaluated",
        "results": results,
    }, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if not output.parent.is_dir():
        raise ValueError("The output directory must already exist.")
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for result in results:
            row = {field: result.get(field) for field in CSV_FIELDS}
            sd = result["standard_uncertainty_nm"]
            for field in ("area_nm", "centroid_nm", "lambda_v2_nm", "delta_lambda_nm"):
                row["u_" + field] = None if sd is None else sd[field]
            row["covariance_area_delta_nm2"] = (None if result["covariance_nm2"] is None
                                                 else result["covariance_nm2"][0][3])
            row["interval_start_nm"], row["interval_end_nm"] = result["interval_nm"]
            writer.writerow(row)
    details.write_text(rendered, encoding="utf-8")
    return output, details


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("delta_results.csv"))
    uncertainty = parser.add_mutually_exclusive_group()
    uncertainty.add_argument("--u-reflectance", type=float,
                             help="Supplied constant standard uncertainty; independent nodes assumed.")
    uncertainty.add_argument("--uncertainty-csv", type=Path,
                             help="Standard uncertainties per node; same layout and grid as input CSV.")
    uncertainty.add_argument("--covariance-json", type=Path,
                             help="Full reflectance covariance matrix for each spectrum ID.")
    parser.add_argument("--reflectance-unit", choices=("fraction", "percent"), default="fraction")
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--decimal", choices=(".", ","), default=".")
    parser.add_argument("--interval", nargs=2, type=float, default=[380., 730.], metavar=("START", "END"))
    parser.add_argument("--integration", choices=("piecewise_linear", "point_trapezoid"), default="piecewise_linear")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        results = process_spectral_series(
            args.input_csv, standard_uncertainty=args.u_reflectance,
            uncertainty_csv=args.uncertainty_csv, covariance_json=args.covariance_json,
            reflectance_unit=args.reflectance_unit, delimiter=args.delimiter,
            decimal=args.decimal, interval_nm=args.interval, integration=args.integration)
        outputs = write_results(results, args.output,
                                input_paths=[args.input_csv, args.uncertainty_csv, args.covariance_json],
                                overwrite=args.overwrite)
    except (ValueError, OSError, TypeError) as exc:
        parser.error(str(exc))
    print(f"Evaluated {len(results)} spectrum/spectra. CSV: {outputs[0]}; details: {outputs[1]}")
    if all(result["standard_uncertainty_nm"] is None for result in results):
        print("Measurement uncertainty was not supplied: blank CSV fields / JSON null mean unknown, not zero.")
    else:
        print("Uncertainty covers supplied reflectance errors at fixed wavelength nodes only; first-order propagation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
