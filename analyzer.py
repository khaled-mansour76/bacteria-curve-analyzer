import numpy as np
import pandas as pd
from config import CHANNELS,SMOOTHING_WINDOW,MIN_RELATIVE_SEPARATION,COMPARISON_METHOD

def load(path):
    d=pd.read_csv(path)
    if "time" not in d: d.insert(0,"time",np.arange(len(d)))
    missing=[c for c in CHANNELS if c not in d]
    if missing: raise ValueError("Missing columns: "+", ".join(missing))
    for c in CHANNELS: d[c]=pd.to_numeric(d[c],errors="coerce")
    return d.dropna(subset=CHANNELS).reset_index(drop=True)

def smooth(x):
    if SMOOTHING_WINDOW<=1:return x
    return pd.Series(x).rolling(SMOOTHING_WINDOW,center=True,min_periods=1).mean().to_numpy()

def norm(x):
    a,b=x.min(),x.max()
    return np.zeros_like(x,dtype=float) if a==b else (x-a)/(b-a)

def compare(a,b):
    mse=float(np.mean((a-b)**2))
    corr=0 if np.std(a)==0 or np.std(b)==0 else float(np.corrcoef(a,b)[0,1])
    if COMPARISON_METHOD=="mse": score=mse
    elif COMPARISON_METHOD=="correlation": score=1-corr
    else: score=.5*mse+.25*(1-corr)
    return score,mse,corr

def analyze(path):
    d=load(path)
    n=d.copy()
    for c in CHANNELS:n[c]=norm(smooth(n[c].to_numpy()))
    r=n.resistance_reference.to_numpy(); s=n.sensitivity_reference.to_numpy()
    rows=[]
    for i in range(1,7):
        t=n[f"test_{i}"].to_numpy()
        sr,mr,cr=compare(t,r); ss,ms,cs=compare(t,s)
        sep=(max(sr,ss)-min(sr,ss))/max(sr,ss) if max(sr,ss) else 0
        result="INCONCLUSIVE" if sep<MIN_RELATIVE_SEPARATION else ("RESISTANT" if sr<ss else "SENSITIVE")
        rows.append([f"test_{i}",sr,ss,mr,ms,cr,cs,result])
    return n,pd.DataFrame(rows,columns=["test","resistance_score","sensitivity_score","mse_resistance","mse_sensitivity","corr_resistance","corr_sensitivity","result"])

if __name__=="__main__":
    import sys
    n,r=analyze(sys.argv[1] if len(sys.argv)>1 else "demo_data.csv")
    r.to_csv("analysis_results.csv",index=False)
    print(r.to_string(index=False))
