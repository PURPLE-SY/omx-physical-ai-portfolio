#!/usr/bin/env python3
"""No motor, no camera. Closed-loop approximation of the run: state fed to the policy = the last command sent (perfect
tracking), images = the recorded frame whose recorded state is nearest that command. Chunk of 100 executed through
smooth 0.3 -> lf01 joint limits -> step cap 3. Reports the jump between the last command and the new chunk's first
action at every chunk change (what the arm would be asked to do right after each 0.5 s inference pause)."""
import json, glob, sys
import numpy as np, pandas as pd, torch
sys.path.insert(0, "/home/purple/omx_logs/b-f01-act-run-20261126")
from offline_dryrun_lib import load_episode, policy, J, lo, hi
pol, pre, post = policy()
PICK = [(f"pick_place_L_11_23_F01_S0{i}", 3) for i in range(1, 7)] + [("pick_place_L_11_24_F01_S01", 1), ("pick_place_L_11_24_F01_S04", 2)]
res = {}
for ds, ep in PICK:
    S, A, F = load_episode(ds, ep); n = len(S)
    cmd = S[0].astype(float).copy(); y = cmd[:5].copy(); jumps, sent, clipped, capped = [], [], 0, 0
    for c in range(int(np.ceil(n / 100)) + 1):
        d = np.linalg.norm(S[:, :5] - cmd[:5], axis=1); f = int(np.argmin(d))
        obs = {"observation.state": torch.tensor(cmd, dtype=torch.float32).unsqueeze(0),
               **{f"observation.images.{k}": torch.from_numpy(F[k][f]).permute(2, 0, 1).float().unsqueeze(0) / 255 for k in F}}
        with torch.inference_mode():
            b = pre(obs); ch = pol.predict_action_chunk(b)
            ch = post(ch).squeeze(0).numpy()
        if c > 0: jumps.append((np.abs(ch[0] - cmd)).round(2).tolist())
        for a in ch:
            y = y + 0.3 * (a[:5] - y); g = np.concatenate([np.clip(y, lo, hi), a[5:]]); clipped += int((g[:5] != y).sum())
            dd = np.clip(g - cmd, -3, 3); capped += int((dd != g - cmd).sum()); cmd = cmd + dd; sent.append(cmd.copy())
    sent = np.array(sent); J6 = np.array(jumps)
    wr = (sent[:, 4] + 100) / 200 * 4095
    res[f"{ds.split('_', 3)[-1]}_ep{ep}"] = {"chunks": len(jumps) + 1, "boundary_jump_max": J6.max(0).round(1).tolist(),
        "boundary_jumps_over_10": int((J6[:, :5] > 10).sum()), "joint_limit_clips": clipped, "step_cap_hits": capped,
        "wrist_raw_range": [int(wr.min()), int(wr.max())], "gripper_range": [round(float(sent[:, 5].min()), 1), round(float(sent[:, 5].max()), 1)],
        "end_nearest_frame_frac": round(f / n, 2)}
    print(ds, ep, json.dumps(res[f"{ds.split('_', 3)[-1]}_ep{ep}"]), flush=True)
json.dump(res, open("/home/purple/omx_logs/b-f01-act-run-20261126/closedloop_sim.json", "w"), indent=1)
