#!/usr/bin/env python3
"""Gate 0 recovery qualification. Synthetic data only; not empirical evidence."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

LABEL = "SIMULATED DATA — METHOD VALIDATION ONLY — NOT EMPIRICAL EVIDENCE"

def seed_for(master, scenario, n, rep):
    s=f"{master}|{scenario}|{n}|{rep}".encode()
    return int(hashlib.sha256(s).hexdigest()[:16],16) % (2**32)

def calibrate(score, noise, target):
    if target == 0: return 0.0
    base=np.mean(np.abs(noise))
    lo,hi=0.0,1.0
    def gain(x): return 1-base/np.mean(np.abs(noise+x*score))
    while gain(hi)<target and hi<1e4: hi*=2
    for _ in range(50):
        mid=(lo+hi)/2
        if gain(mid)<target: lo=mid
        else: hi=mid
    return (lo+hi)/2

def pairs_in(indices, X, k=5):
    if len(indices)<k+1: return np.empty((0,2),int)
    nn=NearestNeighbors(n_neighbors=k+1).fit(X[indices])
    near=nn.kneighbors(X[indices],return_distance=False)[:,1:]
    pairs={tuple(sorted((int(indices[i]),int(indices[j])))) for i,row in enumerate(near) for j in row}
    return np.array(sorted(pairs),int)

def pair_block(X,p): return np.hstack((X[p[:,0]],X[p[:,1]],np.abs(X[p[:,1]]-X[p[:,0]])))

def fit_predict(Xtr,ytr,Xte):
    sc=StandardScaler().fit(Xtr); a=sc.transform(Xtr); b=sc.transform(Xte)
    # Fixed qualification grid; selection uses training data only.
    best=None
    cut=np.arange(len(ytr))%5
    for alpha in (0.1,1,10,100):
        losses=[]
        for f in range(5):
            m=Ridge(alpha=alpha).fit(a[cut!=f],ytr[cut!=f])
            losses.append(mean_absolute_error(ytr[cut==f],m.predict(a[cut==f])))
        if best is None or np.mean(losses)<best[0]: best=(np.mean(losses),alpha)
    return Ridge(alpha=best[1]).fit(a,ytr).predict(b)

def replicate(scenario,n,rep,master=20260831):
    rng=np.random.default_rng(seed_for(master,scenario,n,rep))
    B=rng.normal(size=(n,8)); A=0.35*B[:,:5]+rng.normal(size=(n,5))
    T=0.25*A+0.15*B[:,:5]+rng.normal(size=(n,5))
    folds=np.array([int(hashlib.sha256(f"R{i}".encode()).hexdigest()[:8],16)%5 for i in range(n)])
    ref_u=rng.normal(scale=np.sqrt(.1),size=n)
    fold_metrics=[]
    for held in range(5):
        train=np.flatnonzero(folds!=held); test=np.flatnonzero(folds==held)
        ptr=pairs_in(train,B); pte=pairs_in(test,B)
        blocks_tr=[pair_block(x,ptr) for x in (B,A,T)]
        blocks_te=[pair_block(x,pte) for x in (B,A,T)]
        coef_b=rng.normal(size=blocks_tr[0].shape[1]); coef_b/=np.linalg.norm(coef_b)
        coef_a=rng.normal(size=blocks_tr[1].shape[1]); coef_a/=np.linalg.norm(coef_a)
        coef_t=rng.normal(size=blocks_tr[2].shape[1]); coef_t/=np.linalg.norm(coef_t)
        base_tr=blocks_tr[0]@coef_b; base_te=blocks_te[0]@coef_b
        ga_tr=blocks_tr[1]@coef_a; ga_te=blocks_te[1]@coef_a
        gt_tr=blocks_tr[2]@coef_t; gt_te=blocks_te[2]@coef_t
        eps_tr=rng.normal(size=len(ptr))+ref_u[ptr].sum(axis=1)
        eps_te=rng.normal(size=len(pte))+ref_u[pte].sum(axis=1)
        ag=calibrate(ga_tr,eps_tr,0.10 if scenario in ("S1_GLOBAL","S2_TOPOLOGY") else 0)
        at=calibrate(gt_tr,eps_tr,0.02 if scenario=="S2_TOPOLOGY" else 0)
        ytr=base_tr+ag*ga_tr+at*gt_tr+eps_tr; yte=base_te+ag*ga_te+at*gt_te+eps_te
        X1tr=blocks_tr[0]; X1te=blocks_te[0]
        X2tr=np.hstack(blocks_tr[:2]); X2te=np.hstack(blocks_te[:2])
        X3tr=np.hstack(blocks_tr); X3te=np.hstack(blocks_te)
        mae=[mean_absolute_error(yte,fit_predict(x,ytr,z)) for x,z in ((X1tr,X1te),(X2tr,X2te),(X3tr,X3te))]
        fold_metrics.append(mae)
    m=np.mean(fold_metrics,axis=0)
    g1=1-m[1]/m[0]; g3=1-m[2]/m[1]
    h1=g1>=.10; h3=h1 and g3>=.02
    decision="S2_TOPOLOGY" if h3 else ("S1_GLOBAL" if h1 else "S0_NULL")
    return decision,float(g1),float(g3)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--replicates",type=int,default=50); ap.add_argument("--output",type=Path,required=True); args=ap.parse_args()
    ns=(100,400,800); scenarios=("S0_NULL","S1_GLOBAL","S2_TOPOLOGY")
    cells=[]
    for n in ns:
        for s in scenarios:
            out=[replicate(s,n,r) for r in range(args.replicates)]
            counts={x:sum(z[0]==x for z in out) for x in scenarios}
            cells.append({"n_references":n,"truth":s,"replicates":args.replicates,"decisions":counts,
                          "correct_recovery_rate":counts[s]/args.replicates,
                          "mean_H1_mae_gain":float(np.mean([z[1] for z in out])),"mean_H3_mae_gain":float(np.mean([z[2] for z in out]))})
    result={"label":LABEL,"status":"GATE_0_IMPLEMENTATION_QUALIFICATION","design":"LINEAR_GAUSSIAN_ICC_0.10",
            "cells":cells,"gate_pass":all(c["correct_recovery_rate"]>=.70 for c in cells if c["n_references"]>=400),
            "limitations":["Qualification subset only; not the full locked simulation grid.","Threshold recovery only; full bootstrap and permutation stages remain pending."]}
    args.output.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
