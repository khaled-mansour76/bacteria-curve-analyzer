import argparse,csv,re,time,serial
from config import BAUD_RATE,CHANNELS
def nums(line):
    x=[float(v) for v in re.findall(r"-?\d+(?:\.\d+)?",line)]
    return x if len(x)==8 else None
p=argparse.ArgumentParser()
p.add_argument("--port",required=True);p.add_argument("--baud",type=int,default=BAUD_RATE);p.add_argument("--output",default="data.csv")
a=p.parse_args(); ser=serial.Serial(a.port,a.baud,timeout=1); time.sleep(2)
with open(a.output,"w",newline="") as f:
    w=csv.writer(f);w.writerow(["time"]+CHANNELS);i=0
    try:
        while True:
            line=ser.readline().decode(errors="ignore").strip();v=nums(line)
            if v is not None:w.writerow([i]+v);f.flush();print(i,v);i+=1
    except KeyboardInterrupt:pass
ser.close()
