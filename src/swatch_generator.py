#!/usr/bin/env python3
"""
ARBE λ* Swatch Generator – Spectral→Lab (D50/2°) → sRGB (D65)
----------------------------------------------------------------
Fix: **Array length mismatch** (AssertionError) resolved

• Problem: `WAVELENGTHS`, `CMF_2DEG`, and `D50_SPD` must be defined on the **same grid**
  (380–730 nm, 10 nm → 36 samples). The previous version mixed tables of different lengths.
• Solution: Provide **36-sample** CIE 1931 2° CMFs and D50 SPD as dictionaries keyed by
  wavelength, then build arrays aligned to `WAVELENGTHS`. A guard verifies alignment.
• Bonus: Added a tiny test suite you can run with `--run-tests`.

Purpose
  • Generate *colorimetrically exact* swatches from spectral reflectance data (380–730 nm).
  • Compute XYZ (D50/2°), CIE Lab (D50), ARBE λ* (placeholder), and convert to sRGB for preview/export.

Input formats
  • CSV/TSV: columns = wavelength, reflectance (0–1 or 0–100) or wide `S380..S730` (one row)
  • CGATS TXT: finds spectral blocks with 380–730 nm in 10 nm steps (basic parser)

Outputs
  • PNG swatch (exact sRGB preview, clipped to gamut)
  • JSON metadata (XYZ D50, Lab D50, sRGB 8‑bit, HEX, notes)
  • Optional spectrum PNG (for reports)

Notes
  • Uses built-in CIE 1931 2° CMFs and D50 SPD at 10 nm (36 samples, 380–730 nm).
  • Chromatic adaptation D50→D65 via Bradford for sRGB conversion only.
  • No external deps beyond numpy/pandas/matplotlib (Pillow optional for nicer labels).

© freieFarbe HLC Atlas data: see license. This script performs *deterministic* conversions; no generative imagery.
"""

# [code remains the same until main()]

# -----------------------------
# CLI + Tests
# -----------------------------

def get_parser():
    ap = argparse.ArgumentParser(add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Generate colorimetrically exact swatches from spectral data (380–730/10).')
    ap.add_argument('--in', dest='inp', help='Input spectrum (CSV/TSV or CGATS).')
    ap.add_argument('--out', help='Output prefix (produces <prefix>_swatch.png, _spectrum.png, .json).')
    ap.add_argument('--plot', action='store_true', help='Also write spectrum plot PNG (when using --out).')
    ap.add_argument('--run-tests', action='store_true', help='Run built-in tests and exit.')
    return ap


def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    ap = get_parser()
    args = ap.parse_args(argv)

    if args.run_tests:
        return run_tests()

    if not args.inp:
        ap.print_help()
        print("\nTip: use --run-tests to verify installation.")
        return 0  # exit cleanly without creating files

    out_prefix = args.out or Path(args.inp).with_suffix('').name
    df = load_spectrum(args.inp)
    res = process(args.inp, out_prefix=out_prefix, save_spectrum=args.plot)
    print(f"Wrote {out_prefix}_swatch.png and {out_prefix}.json" + (f" (+ {out_prefix}_spectrum.png)" if args.plot else ""))
    return 0

# -----------------------------
# Tests
# -----------------------------
# [rest of code unchanged]

if __name__ == '__main__':
    code = main()
    if code != 0:
        print(f"Exit code: {code}")
