import sys
from pathlib import Path
import matplotlib.pyplot as plt
from analyzer import analyze
path=sys.argv[1] if len(sys.argv)>1 else "demo_data.csv"
out=Path("report");out.mkdir(exist_ok=True)
n,r=analyze(path)
plt.figure(figsize=(10,6))
plt.plot(n.time,n.resistance_reference,label="Resistance reference")
plt.plot(n.time,n.sensitivity_reference,label="Sensitivity reference")
for i in range(1,7):plt.plot(n.time,n[f"test_{i}"],alpha=.5,label=f"Test {i}")
plt.xlabel("Time / sample index");plt.ylabel("Normalized RAW");plt.legend(ncol=2);plt.tight_layout()
plt.savefig(out/"all_curves.png",dpi=180);plt.close()
r.to_csv(out/"analysis_results.csv",index=False)
for i,row in r.iterrows():
    plt.figure(figsize=(9,5))
    plt.plot(n.time,n.resistance_reference,label="Resistance reference")
    plt.plot(n.time,n.sensitivity_reference,label="Sensitivity reference")
    plt.plot(n.time,n[f"test_{i+1}"],label=f"Test {i+1}")
    plt.title(f"Test {i+1}: {row.result}");plt.xlabel("Time / sample index");plt.ylabel("Normalized RAW");plt.legend();plt.tight_layout()
    plt.savefig(out/f"test_{i+1}.png",dpi=180);plt.close()
print(r.to_string(index=False))
