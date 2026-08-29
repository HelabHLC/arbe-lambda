#!/usr/bin/env python3
"""ATLAS Clarus x ARBE lambda* Study A pilot.

This is a pipeline check, not confirmatory evidence. It compares a strong
colourimetric baseline with global ARBE descriptors and difference-curve
topology under deterministic, reference-disjoint outer folds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ILLUMINANTS = ("D50", "D65", "A", "LEDB1", "F11")


def delta_e_00(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    """Vectorised CIEDE2000, matching the public ARBE browser implementation."""
    L1, a1, b1 = np.moveaxis(lab1, -1, 0)
    L2, a2, b2 = np.moveaxis(lab2, -1, 0)
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    cbar = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(cbar**7 / (cbar**7 + 25**7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.mod(np.degrees(np.arctan2(b1, a1p)), 360)
    h2p = np.mod(np.degrees(np.arctan2(b2, a2p)), 360)
    h1p = np.where((a1p == 0) & (b1 == 0), 0, h1p)
    h2p = np.where((a2p == 0) & (b2 == 0), 0, h2p)
    dLp, dCp = L2 - L1, C2p - C1p
    raw_dh = h2p - h1p
    dhp = np.where(C1p * C2p == 0, 0, raw_dh)
    dhp = np.where((C1p * C2p != 0) & (raw_dh > 180), raw_dh - 360, dhp)
    dhp = np.where((C1p * C2p != 0) & (raw_dh < -180), raw_dh + 360, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))
    Lbarp, Cbarp = (L1 + L2) / 2, (C1p + C2p) / 2
    hsum, hdiff = h1p + h2p, np.abs(h1p - h2p)
    hbarp = np.where(C1p * C2p == 0, hsum, hsum / 2)
    hbarp = np.where((C1p * C2p != 0) & (hdiff > 180) & (hsum < 360), (hsum + 360) / 2, hbarp)
    hbarp = np.where((C1p * C2p != 0) & (hdiff > 180) & (hsum >= 360), (hsum - 360) / 2, hbarp)
    T = (1 - 0.17*np.cos(np.radians(hbarp-30)) + 0.24*np.cos(np.radians(2*hbarp))
         + 0.32*np.cos(np.radians(3*hbarp+6)) - 0.20*np.cos(np.radians(4*hbarp-63)))
    dtheta = 30 * np.exp(-((hbarp - 275) / 25) ** 2)
    RC = 2 * np.sqrt(Cbarp**7 / (Cbarp**7 + 25**7))
    SL = 1 + 0.015*(Lbarp-50)**2 / np.sqrt(20+(Lbarp-50)**2)
    SC, SH = 1 + 0.045*Cbarp, 1 + 0.015*Cbarp*T
    RT = -np.sin(np.radians(2*dtheta))*RC
    return np.sqrt((dLp/SL)**2 + (dCp/SC)**2 + (dHp/SH)**2 + RT*(dCp/SC)*(dHp/SH))


def xyz_to_lab(xyz: np.ndarray, white: np.ndarray) -> np.ndarray:
    t = xyz / white
    e, k = 216/24389, 24389/27
    f = np.where(t > e, np.cbrt(t), (k*t+16)/116)
    return np.column_stack((116*f[:, 1]-16, 500*(f[:, 0]-f[:, 1]), 200*(f[:, 1]-f[:, 2])))


def lab_from_weights(R: np.ndarray, rows: list[dict]) -> np.ndarray:
    W = np.array([[r["X"], r["Y"], r["Z"]] for r in rows], dtype=float)
    return xyz_to_lab(R @ W, np.ones((1, 36)) @ W)


def topology_features(diff: np.ndarray) -> np.ndarray:
    eps = 1e-9
    sign = np.where(np.abs(diff) <= eps, 0, np.sign(diff))
    crossing = np.sum(sign[:, :-1] * sign[:, 1:] < 0, axis=1)
    equal = np.sum(sign == 0, axis=1)
    return np.column_stack((
        crossing, equal, np.sum(np.abs(diff), axis=1)*10,
        np.sum(diff, axis=1)*10, np.max(np.abs(diff), axis=1),
        np.sqrt(np.mean(diff**2, axis=1)), np.mean(np.abs(diff), axis=1),
    ))


def stable_fold(reference: str, folds: int = 5) -> int:
    return int(hashlib.sha256(reference.encode()).hexdigest()[:8], 16) % folds


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, required=True)
    ap.add_argument("--weights-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()

    raw = args.index.read_bytes()
    index = json.loads(raw)
    records = index["records"]
    assert index["record_count"] == len(records) == 13283
    refs = np.array([r["reference"] for r in records])
    assert len(set(refs)) == len(refs)
    R = np.array([r["R"] for r in records], dtype=float)
    assert R.shape == (13283, 36) and np.isfinite(R).all()
    folds = np.array([stable_fold(r) for r in refs])
    labs = {}
    weight_hashes = {}
    for ill in ILLUMINANTS:
        p = args.weights_dir / f"weights_{ill}_1931.json"
        blob = p.read_bytes(); weight_hashes[ill] = hashlib.sha256(blob).hexdigest()
        data = json.loads(blob)
        assert len(data["rows"]) == 36
        labs[ill] = lab_from_weights(R, data["rows"])

    pairs = []
    for fold in range(5):
        idx = np.flatnonzero(folds == fold)
        nn = NearestNeighbors(n_neighbors=args.k+1).fit(labs["D50"][idx])
        _, neighbours = nn.kneighbors(labs["D50"][idx])
        unique = {tuple(sorted((int(idx[i]), int(idx[j])))) for i, row in enumerate(neighbours[:, 1:]) for j in row}
        pairs.extend((a, b, fold) for a, b in sorted(unique))
    ia, ib, pair_fold = map(np.array, zip(*pairs))

    d50 = delta_e_00(labs["D50"][ia], labs["D50"][ib])
    alternate = np.column_stack([delta_e_00(labs[x][ia], labs[x][ib]) for x in ILLUMINANTS[1:]])
    y = np.max(alternate - d50[:, None], axis=1)
    labdiff = labs["D50"][ib] - labs["D50"][ia]
    baseline = np.column_stack((d50, np.abs(labdiff), np.linalg.norm(labdiff[:, 1:], axis=1)))
    keys = ("lambda_v2_nm", "lambda_ee_nm", "delta_lambda_nm", "mu2_nm2", "sigma_star_nm", "mu3_nm3", "skewness_gamma1")
    global_values = np.array([[r["lambda"][k] for k in keys] for r in records], dtype=float)
    global_pair = np.abs(global_values[ib] - global_values[ia])
    topology = topology_features(R[ib] - R[ia])
    models = {"M1_colourimetry": baseline, "M2_global_ARBE": np.column_stack((baseline, global_pair)),
              "M3_ARBE_topology": np.column_stack((baseline, global_pair, topology))}

    rows = []
    for held_out in range(5):
        test = pair_fold == held_out; train = ~test
        inner = GroupKFold(n_splits=4)
        for name, X in models.items():
            search = GridSearchCV(make_pipeline(StandardScaler(), Ridge()),
                                  {"ridge__alpha": [0.01, 0.1, 1, 10, 100]},
                                  scoring="neg_mean_absolute_error",
                                  cv=inner.split(X[train], y[train], groups=pair_fold[train]))
            search.fit(X[train], y[train])
            pred = search.predict(X[test])
            rows.append({"fold": held_out, "model": name, "n_test": int(test.sum()),
                         "mae": float(mean_absolute_error(y[test], pred)),
                         "r2": float(r2_score(y[test], pred)),
                         "alpha": float(search.best_params_["ridge__alpha"])})

    summary = {}
    for name in models:
        selected = [r for r in rows if r["model"] == name]
        summary[name] = {"mean_mae": float(np.mean([r["mae"] for r in selected])),
                         "mean_r2": float(np.mean([r["r2"] for r in selected]))}
    base_mae = summary["M1_colourimetry"]["mean_mae"]
    for name in summary:
        summary[name]["mae_reduction_vs_M1_pct"] = 100*(base_mae-summary[name]["mean_mae"])/base_mae

    result = {"status": "PILOT_PIPELINE_CHECK_NOT_CONFIRMATORY", "index_sha256": hashlib.sha256(raw).hexdigest(),
              "weight_sha256": weight_hashes, "record_count": len(records), "pair_count": len(pairs),
              "fold_reference_counts": np.bincount(folds, minlength=5).tolist(), "endpoint": "IIS pair divergence vs D50",
              "models": summary, "fold_results": rows,
              "limitations": ["Analysis choices were not preregistered before this pilot.",
                              "Predictors and endpoint derive from the same atlas spectra; physical causality is not established.",
                              "External measured samples remain mandatory for industrial claims."]}
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
