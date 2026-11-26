import os, json, csv, hashlib
from huggingface_hub import HfApi
a=HfApi(); L="/home/purple/omx_datasets/"; O="/home/purple/omx_reports/hf_inventory_20261127/"
local=list(csv.DictReader(open(O+"local_datasets.csv")))
hf={r["repo"].split("/")[1]:r for r in csv.DictReader(open(O+"hf_repos.csv")) if r["kind"]=="dataset"}
pairs=[]
for r in local:
    if r["root"]!="local": continue
    p=r["path"]; n=os.path.basename(p); cand=None; prefix=""
    if n in hf: cand=n
    elif n.startswith("pick_place_11_14_S") and "spot" not in n:
        cand="pick_place_left_11_14_"+n.replace("pick_place_11_14_","").rstrip("_")
        if n=="pick_place_11_14_S01_F03": cand=None
    elif p=="front/pick_place_v1": cand="omx-front-arm"
    elif p=="front/pick_place_v2": cand="omx-front-arm-v2"
    elif n=="pick_place_11_04LEFT": cand="omx-left-arm-20261104"
    elif p.startswith("left/wrist_degrees/"):
        v=n.replace("pick_place_","")
        m={"10월 31일 모방 학습!":"2026-10-31_v19","v20":"2026-10-31_v20","v22":"2026-11-02_v22","v23":"2026-11-02_v23","v24":"2026-11-03_v24","v25":"2026-11-03_v25"}
        if n in m: cand,prefix="omx-left-arm",m[n]
        elif v in m: cand,prefix="omx-left-arm",m[v]
    if cand and cand in hf: pairs.append((p,cand,prefix))
def sha256(f):
    h=hashlib.sha256()
    with open(f,"rb") as fh:
        for b in iter(lambda: fh.read(1<<22), b""): h.update(b)
    return h.hexdigest()
def gitsha(f):
    d=open(f,"rb").read(); return hashlib.sha1(b"blob %d\0"%len(d)+d).hexdigest()
res=[]
for p,repo,prefix in pairs:
    if p=="left/wrist_degrees/pick_place_v19": continue  # symlink to 10월 31일 folder
    base=L+p; ok=bad=miss=0; badl=[]; hfpaths=set()
    for x in a.list_repo_tree("Purple-SY/"+repo,repo_type="dataset",recursive=True,path_in_repo=prefix or None):
        if not hasattr(x,"blob_id"): continue
        rel=x.path[len(prefix)+1:] if prefix else x.path
        hfpaths.add(rel)
        if rel in (".gitattributes","README.md") or rel.startswith("에피소드별") or rel.endswith(".txt") or rel.endswith("목록.json"): continue
        lp=os.path.join(base,rel)
        if not os.path.exists(lp): miss+=1; badl.append("hf-only "+rel); continue
        g=(sha256(lp)==x.lfs.sha256) if x.lfs else (gitsha(lp)==x.blob_id)
        ok+=g; bad+=not g
        if not g: badl.append("diff "+rel)
    localonly=[os.path.relpath(os.path.join(dp,f),base) for dp,_,fs in os.walk(base) for f in fs]
    localonly=[f for f in localonly if f not in hfpaths and not f.startswith(".cache")]
    res.append(dict(local=p,repo=repo+("/"+prefix if prefix else ""),ok=ok,diff=bad,hf_only=miss,local_only=len(localonly),notes=(badl+["local-only "+f for f in localonly])[:6]))
    print(p,"->",repo,prefix,"ok",ok,"diff",bad,"hf_only",miss,"local_only",len(localonly),flush=True)
json.dump(res,open(O+"sha_verify_existing.json","w"),indent=1,ensure_ascii=False)
print("DONE",len(res))
