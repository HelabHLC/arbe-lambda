# PET ARBE-C numerical reproduction — preliminary

**Status (2026-11-12):** The published PET illustration can be **numerically reproduced from the two derived group-median spectra**, but raw-data lineage and sample independence have **not** been independently audited. Do not call this a validated ageing study.

## Reproduction

Run `python verify_pet.py derived_pet_block0_block1.csv` with Python 3 (no external dependencies). The required CSV columns are `wavelength_nm,median_block0,median_block1,difference,centered_difference,C_nm`, sampled at 1 nm from 380 through 730 nm inclusive.

The derived CSV is available in the companion downloadable reproduction package supplied with the research discussion; **it has not yet been committed to GitHub**. Its SHA-256 is `1d9b27766282a7b2dbb078e982821ddf157a9943ed46716b768b0bf3dab9d3d4` (27,496 bytes).

**Expected results:** maximum absolute local difference at **730 nm** (boundary); maximum absolute centered cumulative excursion at **639 nm**; **K = 0.0961048 nm**, rounded in the article to **0.096105 nm**; C(730) approximately zero.

## Derivation and provenance

The local figure-generation script used an embedded 21-block PET 5 mm, no-glass data structure, with five technical replicates per block. It selected adjacent **block indices 0 and 1**, computed the wavelength-wise **median** of each group, then took their difference. The source was identified as the **de-Vries** spectral dataset. This comparison is **not a verified before/after ageing pair**.

Local source files examined during preparation (not redistributed here):
- `L0_SE_Raw_Cleaned_Datafiles.zip`: 30,370,989 bytes; SHA-256 `884a1db1759f0be3ead5c6822655ffc613b854099524187621fbf0160f6b0204`
- `L0_SE_Raw_Metadata.csv`: 20,806 bytes; SHA-256 `73f622fcecf2671d6971bc616adae5c724fc5739481c8e82085e3144a5d228bf`
- `de_vries_spectral_metadata_mapping.csv`: 307,797 bytes; SHA-256 `69e1c098d5b319d303ed4933757a4bd75757ec69bc3ac032a942f2a7e58ad1a2`

**Raw-to-median lineage now checked:** [the raw-lineage audit](raw_lineage_audit.md) identifies all ten original SED filenames and their two metadata groups; [the independent raw-file verification script](verify_raw_lineage.py) reproduces both 351-point medians exactly from the original archive. **Still outstanding:** source licensing/redistribution rights, external verification of the measurement conditions and an independently validated material-change endpoint. Technical replicates must not be treated as independent biological/material samples. The local metadata audit identifies PET 5 mm without glass as 105 spectra across 21 depth blocks; depth is not ageing time.

This package demonstrates **computational consistency**, not diagnostic superiority over RMS, total variation, or other established methods.
