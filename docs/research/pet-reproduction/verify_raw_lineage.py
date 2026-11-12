#!/usr/bin/env python3
"""Verify the two PET medians directly from ten original de-Vries SED files.
Usage: python verify_raw_lineage.py L0_SE_Raw_Cleaned_Datafiles.zip derived_pet_block0_block1.csv
Standard library only; input ZIP must be obtained lawfully from its original source.
"""
import csv, hashlib, io, re, statistics, sys, zipfile
from pathlib import Path

zip_path, csv_path = map(Path, sys.argv[1:3])
expected_zip_sha256 = "884a1db1759f0be3ead5c6822655ffc613b854099524187621fbf0160f6b0204"
actual_sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()
assert actual_sha256 == expected_zip_sha256, "Raw ZIP checksum mismatch"
prefix = "2021_Sep_01_SR-3501_SN19387Q4__"
groups = [[141,142,143,144,145], [156,157,158,159,160]]
wavelengths = list(range(380,731))
with zipfile.ZipFile(zip_path) as z:
    medians=[]
    for group in groups:
        spectra=[]
        for number in group:
            name=f"{prefix}{number:05d}.sed"
            lines=z.read(name).decode("latin1").splitlines()
            vals={}
            for line in lines:
                m=re.fullmatch(r"\s*(\d+\.\d+)\s+([+\-]?(?:\d+\.?\d*|\.\d+)(?:[Ee][+\-]?\d+)?)\s*",line)
                if m: vals[int(float(m.group(1)))] = float(m.group(2))
            assert all(w in vals for w in wavelengths), name
            spectra.append([vals[w] for w in wavelengths])
        medians.append([statistics.median(v) for v in zip(*spectra)])
with csv_path.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
assert len(rows)==351
for i,row in enumerate(rows):
    assert int(row["wavelength_nm"])==wavelengths[i]
    for j in (0,1):
        assert float(row[f"median_block{j}"])==medians[j][i],(i,j)
print("PASS: 10 original SED files mapped to groups 141–145 and 156–160.")
print("PASS: 351/351 median values agree exactly for both groups.")
print("NOTE: depth contrast 0 vs 5 mm; NOT a confirmed ageing before/after pair.")
