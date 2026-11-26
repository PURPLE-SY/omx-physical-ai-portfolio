#!/usr/bin/env python3
"""No motor, no camera. B arm F02 wristfix Best 12000: closed-loop approximation per training episode (same method as
b-f01-act-run-20261126/s03_s05_reach.py) for S01-S06 (wristfix data, 60 ep). Grasp pose error <= 6 and place pose
error <= 8 normalized units (1 unit = 1.8 deg) = ok. Joint limits = the F02 kit's safety file (training range +-8)."""
import json, sys
import numpy as np, torch
sys.path.insert(0, "/home/purple/omx_logs/b-f01-act-run-20261126")
import offline_dryrun_lib as L
SAFETY = sys.argv[1]
L.W = "/home/purple/omx_models/omx-act-arm-b-f02-wristfix-best12000-cpu-compat"  # training frames: no camera warp
lim = json.load(open(SAFETY))["joint_limits"]
lo = np.array([lim[j][0] / 4095 * 200 - 100 for j in L.J]); hi = np.array([lim[j][1] / 4095 * 200 - 100 for j in L.J])
pol, pre, post = L.policy()
def chunk(state, imgs):
    obs = {"observation.state": torch.tensor(state, dtype=torch.float32).unsqueeze(0),
           **{f"observation.images.{k}": torch.from_numpy(v).permute(2, 0, 1).float().unsqueeze(0) / 255 for k, v in imgs.items()}}
    with torch.inference_mode():
        return post(pol.predict_action_chunk(pre(obs))).squeeze(0).numpy()
def events(g):
    o = np.where(g > 57)[0]
    if not len(o): return None, None
    c = np.where((g < 51) & (np.arange(len(g)) > o[0]))[0]
    if not len(c): return None, None
    p = np.where((g > 57) & (np.arange(len(g)) > c[0] + 15))[0]
    return int(c[0]), (int(p[0]) if len(p) else None)
res = {}; clips = 0; jumps = []
for s in range(1, 7):
    ds = f"pick_place_Left_11_21_F02_S0{s}_wristfix"
    for ep in range(10):
        S, A, F = L.load_episode(ds, ep)
        rg, rp = events(A[:, 5])
        cmd = S[0].astype(float).copy(); y = cmd[:5].copy(); sent = []; nchunk = int(np.ceil(len(S) / 100)) + 1
        prev = None
        for c in range(nchunk):
            f = int(np.argmin(np.linalg.norm(S[:, :5] - cmd[:5], axis=1)))
            ch = chunk(cmd, {k: F[k][f] for k in F})
            if prev is not None: jumps.append(float(np.abs(ch[0, :5] - prev[:5]).max()))
            for a in ch:
                y = y + 0.3 * (a[:5] - y); clips += int(np.any((y < lo) | (y > hi)))
                g = np.concatenate([np.clip(y, lo, hi), a[5:]])
                cmd = cmd + np.clip(g - cmd, -3, 3); sent.append(cmd.copy())
            prev = ch[-1]
        sent = np.array(sent); sg, sp = events(sent[:, 5])
        r = {"rec_grasp_f": rg, "rec_place_f": rp, "sim_grasp_f": sg, "sim_place_f": sp, "wrist_range": [round(float(sent[:, 4].min()), 1), round(float(sent[:, 4].max()), 1)]}
        if rg is not None and sg is not None: r["grasp_pose_err"] = round(float(np.abs(sent[sg, :5] - A[rg, :5]).max()), 1)
        if rp is not None and sp is not None: r["place_pose_err"] = round(float(np.abs(sent[sp, :5] - A[rp, :5]).max()), 1)
        r["grasp_ok"] = r.get("grasp_pose_err", 99) <= 6
        r["ok"] = r["grasp_ok"] and r.get("place_pose_err", 99) <= 8
        res[f"S0{s}_ep{ep}"] = r; print(f"S0{s} ep{ep}", json.dumps(r), flush=True)
summ = {}
for s in range(1, 7):
    r = [v for k, v in res.items() if k.startswith(f"S0{s}")]
    ge = [v["grasp_pose_err"] for v in r if "grasp_pose_err" in v]; pe = [v["place_pose_err"] for v in r if "place_pose_err" in v]
    summ[f"S0{s}"] = {"episodes": len(r), "grasp_ok": sum(v["grasp_ok"] for v in r), "ok": sum(v["ok"] for v in r),
                      "grasp_err_median": round(float(np.median(ge)), 1) if ge else None, "place_err_median": round(float(np.median(pe)), 1) if pe else None}
summ["_all"] = {"joint_limit_hits": clips, "chunk_jump_max": round(max(jumps), 2) if jumps else None}
res["_summary"] = summ; print(json.dumps(summ, ensure_ascii=False))
json.dump(res, open("/home/purple/omx_logs/b-f02-ex-prep-20261126/f02_spot_reach.json", "w"), indent=1)
