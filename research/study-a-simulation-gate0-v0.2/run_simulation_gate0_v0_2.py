#!/usr/bin/env python3
"""Simulation Protocol v0.2 Gate 0. Synthetic method validation only."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from joblib import Parallel, delayed
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

LABEL="SIMULATED DATA — METHOD VALIDATION ONLY — NOT EMPIRICAL EVIDENCE"
SCENARIOS={"S0_NULL":(0.,0.),"S1_GLOBAL":(.15,0.),"S2_TOPOLOGY":(.15,.05)}

def seed_for(*parts): return int(hashlib.sha256("|".join(map(str,parts)).encode()).hexdigest()[:16],16)%(2**32)
def pairs(idx,B,k=5):
    if len(idx)<k+1:return np.empty((0,2),int)
    near=NearestNeighbors(n_neighbors=k+1).fit(B[idx]).kneighbors(B[idx],return_distance=False)[:,1:]
    return np.array(sorted({tuple(sorted((int(idx[i]),int(idx[j])))) for i,row in enumerate(near) for j in row}),int)
def block(X,p): return np.hstack((X[p[:,0]],X[p[:,1]],np.abs(X[p[:,1]]-X[p[:,0]])))
def fit_pred(X,y,Z):
    s=StandardScaler().fit(X); return Ridge(alpha=10.).fit(s.transform(X),y).predict(s.transform(Z))
def gain(y,p0,p1): return 1-mean_absolute_error(y,p1)/mean_absolute_error(y,p0)

def calibrate(target,base_fit,extra_fit,noise_fit,base_eval,extra_eval,noise_eval,prior_fit=None,prior_eval=None):
    if target==0:return 0.,0.
    lo,hi=0.,1.
    def measured(a):
        yf=base_fit+noise_fit+a*extra_fit; ye=base_eval+noise_eval+a*extra_eval
        X0=base_fit[:,None] if prior_fit is None else prior_fit
        Z0=base_eval[:,None] if prior_eval is None else prior_eval
        X1=np.column_stack((X0,extra_fit)); Z1=np.column_stack((Z0,extra_eval))
        return gain(ye,fit_pred(X0,yf,Z0),fit_pred(X1,yf,Z1))
    while measured(hi)<target and hi<128:hi*=2
    for _ in range(18):
        mid=(lo+hi)/2
        if measured(mid)<target:lo=mid
        else:hi=mid
    a=(lo+hi)/2
    return a,measured(a)

def replicate(scenario,n,rep,master=20260903):
    rng=np.random.default_rng(seed_for(master,scenario,n,rep))
    B=rng.normal(size=(n,8)); A=.35*B[:,:5]+rng.normal(size=(n,5)); T=.25*A+.15*B[:,:5]+rng.normal(size=(n,5))
    order=rng.permutation(n); ncal=int(.2*n); ntrain=int(.6*n)
    cal,train,test=order[:ncal],order[ncal:ncal+ntrain],order[ncal+ntrain:]
    csplit=len(cal)//2; cfit,ceval=cal[:csplit],cal[csplit:]
    parts={k:pairs(v,B) for k,v in (("cf",cfit),("ce",ceval),("tr",train),("te",test))}
    coef=[rng.normal(size=d) for d in (24,15,15)]; coef=[x/np.linalg.norm(x) for x in coef]
    data={}
    ref_u=rng.normal(scale=np.sqrt(.1),size=n)
    for key,p in parts.items():
        b,a,t=block(B,p),block(A,p),block(T,p)
        bs=b@coef[0]; gs=a@coef[1]; ts=t@coef[2]
        noise=rng.normal(size=len(p))+ref_u[p].sum(axis=1)
        data[key]=(b,a,t,bs,gs,ts,noise)
    tg,tt=SCENARIOS[scenario]
    cf,ce=data["cf"],data["ce"]
    ag,cal_g=calibrate(tg,cf[3],cf[4],cf[6],ce[3],ce[4],ce[6],cf[0],ce[0])
    # Topology calibration compares B+A against B+A+T after global injection.
    basef=cf[3]+ag*cf[4]; basee=ce[3]+ag*ce[4]
    priorf=np.hstack((cf[0],cf[1])); priore=np.hstack((ce[0],ce[1]))
    at,cal_t=calibrate(tt,basef,cf[5],cf[6],basee,ce[5],ce[6],priorf,priore)
    tr,te=data["tr"],data["te"]
    ytr=tr[3]+ag*tr[4]+at*tr[5]+tr[6]; yte=te[3]+ag*te[4]+at*te[5]+te[6]
    X1,Z1=tr[0],te[0]; X2,Z2=np.hstack((tr[0],tr[1])),np.hstack((te[0],te[1])); X3,Z3=np.hstack((tr[0],tr[1],tr[2])),np.hstack((te[0],te[1],te[2]))
    p1,p2,p3=fit_pred(X1,ytr,Z1),fit_pred(X2,ytr,Z2),fit_pred(X3,ytr,Z3)
    g1,g3=gain(yte,p1,p2),gain(yte,p2,p3); h1=g1>=.10; h3=h1 and g3>=.02
    decision="S2_TOPOLOGY" if h3 else ("S1_GLOBAL" if h1 else "S0_NULL")
    return {"decision":decision,"observed_H1":g1,"observed_H3":g3,"recoverable_H1":cal_g,"recoverable_H3":cal_t,"a_global":ag,"a_topology":at,
            "partition_sizes":[len(cal),len(train),len(test)],"pair_counts":[len(parts[x]) for x in ("cf","ce","tr","te")]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--replicates",type=int,default=250);ap.add_argument("--jobs",type=int,default=-1);ap.add_argument("--reference-counts",type=int,nargs="+",default=[100,400,800,1600]);ap.add_argument("--output",type=Path,required=True);a=ap.parse_args()
    cells=[]
    for n in a.reference_counts:
        for s in SCENARIOS:
            out=Parallel(n_jobs=a.jobs,batch_size=5)(delayed(replicate)(s,n,r) for r in range(a.replicates))
            counts={x:sum(z["decision"]==x for z in out) for x in SCENARIOS}
            cells.append({"n_references":n,"truth":s,"replicates":a.replicates,"decisions":counts,"correct_recovery_rate":counts[s]/a.replicates,
                          "mean_recoverable_H1":float(np.mean([z["recoverable_H1"] for z in out])),"mean_observed_H1":float(np.mean([z["observed_H1"] for z in out])),
                          "mean_recoverable_H3":float(np.mean([z["recoverable_H3"] for z in out])),"mean_observed_H3":float(np.mean([z["observed_H3"] for z in out]))})
    null=[c for c in cells if c["truth"]=="S0_NULL"]; max_n=max(a.reference_counts); power=[c for c in cells if c["n_references"]==max_n and c["truth"]!="S0_NULL"]
    false_pos=sum(c["replicates"]-c["decisions"]["S0_NULL"] for c in null)/sum(c["replicates"] for c in null)
    result={"label":LABEL,"status":"GATE_0_V0_2_COMPLETE","design":"LINEAR_GAUSSIAN_ICC_0.10","cells":cells,"null_false_positive_rate":false_pos,
            "gate_pass":false_pos<=.075 and all(c["correct_recovery_rate"]>=.80 for c in power),
            "limitations":["Gate 0 core design only; full noise/signal/ICC grid and bootstrap/permutation inference remain pending."]}
    a.output.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":main()
