# PET raw-file lineage audit — 12 November 2026

**Result: PASS for computational raw-to-median lineage; NOT a validation of ageing or diagnostic benefit.**

## Exact source mapping

Dataset: de-Vries reflectance measurements, 1 September 2021; instrument file prefix `2021_Sep_01_SR-3501_SN19387Q4__`. The metadata-to-file mapping associates the following measurements with PET, **5 mm specimen thickness, no glass**:

| Group | Depth in metadata | Metadata index | Original .sed files |
| --- | --- | --- | --- |
| block0 | 0 mm | 248 | 00141, 00142, 00143, 00144, 00145 |
| block1 | 5 mm | 250 | 00156, 00157, 00158, 00159, 00160 |

Each original file contains 1 nm reflectance data. The independent audit read 380–730 nm inclusive, then calculated the **pointwise median of five files per group**. Compared with the previously published `derived_pet_block0_block1.csv`, both median spectra matched **exactly at all 351 wavelengths** (maximum absolute difference **0.0** in source precision).

## Reproduce the raw-file audit

```sh
python verify_raw_lineage.py L0_SE_Raw_Cleaned_Datafiles.zip derived_pet_block0_block1.csv
python verify_pet.py derived_pet_block0_block1.csv
```

Inputs are not redistributed here; the derived CSV is available in the companion reproduction ZIP.

SHA-256:
- Raw archive: `884a1db1759f0be3ead5c6822655ffc613b854099524187621fbf0160f6b0204`
- Metadata mapping: `69e1c098d5b319d303ed4933757a4bd75757ec69bc3ac032a942f2a7e58ad1a2`
- Derived CSV: `1d9b27766282a7b2dbb078e982821ddf157a9943ed46716b768b0bf3dab9d3d4`

## Limits

The mapping is based on the available metadata table and matching original filenames. Source license and independent verification of experimental conditions remain open. **0 and 5 mm are measurement depths, not time points.** These are two groups of technical replicates, not ten independent material specimens. Neither K nor this agreement establishes degradation, causal identification, or superiority over RMS/TV.
