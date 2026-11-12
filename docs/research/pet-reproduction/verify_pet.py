#!/usr/bin/env python3
"""Recompute ARBE-C from the six-column derived PET block-median CSV.
Requires only Python standard library. Does NOT validate raw-data provenance.
"""
import csv, math, sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path("derived_pet_block0_block1.csv")
rows=list(csv.DictReader(p.open(newline="",encoding="utf-8")))
w=[float(r["wavelength_nm"]) for r in rows]
a=[float(r["median_block0"]) for r in rows]
b=[float(r["median_block1"]) for r in rows]
assert len(w)==351 and w==list(range(380,731))
d=[v-u for u,v in zip(a,b)]
mean=sum((d[i]+d[i+1])/2 for i in range(350))/350
c=[0.0]
for i in range(350): c.append(c[-1]+(d[i]+d[i+1]-2*mean)/2)
peak=max(range(351),key=lambda i:abs(d[i]))
ki=max(range(351),key=lambda i:abs(c[i]))
print(f"max local |d| at {w[peak]:.0f} nm")
print(f"max |C| at {w[ki]:.0f} nm; K={abs(c[ki]):.9f} nm; C(730)={c[-1]:.3g}")
assert (w[peak],w[ki])==(730,639)
assert math.isclose(abs(c[ki]),0.0961048,abs_tol=1e-8)
assert abs(c[-1])<1e-10
for r,v in zip(rows,c): assert math.isclose(float(r["C_nm"]),v,abs_tol=1e-10)
print("PASS: derived spectra reproduce the reported PET figure")
