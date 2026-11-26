#!/usr/bin/env python3
"""No motor, no camera. For one episode per F01 folder: recorded frames -> policy (CPU copy, chunk every 100 steps like
the run, observation = recorded state at the chunk start) -> the run's command chain: OMX_RUN_SMOOTH 0.3 (gripper
unfiltered) -> lf01-run joint limits -> max_relative_target 3 vs the last command. Reports chunk-boundary jumps,
step sizes, limit clips, wrist raw range / jumps, MAE vs recorded action, and inference time."""
import json, glob, time, sys
import av, numpy as np, pandas as pd, torch
from lerobot.configs.policies import PreTrainedConfig
from lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.policies.factory import make_pre_post_processors
torch.set_num_threads(4)
K = "/home/purple/omx_logs/b-f01-act-run-20261126"
W = "/home/purple/omx_models/omx-act-arm-b-f01-best12000-cpu-compat"
D = "/home/purple/omx_datasets/"
lim = json.load(open(K + "/safety-1d2d-132a.lf01-run.json"))["joint_limits"]
J = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]
lo = np.array([lim[j][0] / 4095 * 200 - 100 for j in J]); hi = np.array([lim[j][1] / 4095 * 200 - 100 for j in J])
cfg = PreTrainedConfig.from_pretrained(W); pol = ACTPolicy.from_pretrained(W, config=cfg).eval()
pre, post = make_pre_post_processors(cfg, pretrained_path=W, preprocessor_overrides={"device_processor": {"device": "cpu"}})
CAMS = ["bottom", "wrist", "top"]
def frames(ds, row, key, n):
    info = json.load(open(D + ds + "/meta/info.json")); k = f"observation.images.{key}"
    path = D + ds + "/" + info["video_path"].format(video_key=k, chunk_index=int(row[f"videos/{k}/chunk_index"]), file_index=int(row[f"videos/{k}/file_index"]))
    t0 = float(row[f"videos/{k}/from_timestamp"]); out = []
    with av.open(path) as c:
        for fr in c.decode(video=0):
            if fr.time >= t0 - 1e-3:
                out.append(fr.to_ndarray(format="rgb24"))
                if len(out) == n: break
    return out
PICK = [(f"pick_place_L_11_23_F01_S0{i}", 3) for i in range(1, 7)] + [("pick_place_L_11_24_F01_S01", 1), ("pick_place_L_11_24_F01_S04", 2)]
results, tinf = {}, []
for ds, ep in PICK:
    df = pd.concat([pd.read_parquet(f) for f in glob.glob(D + ds + "/data/**/*.parquet", recursive=True)])
    g = df[df.episode_index == ep].sort_values("frame_index")
    S, A = np.stack(g["observation.state"].values), np.stack(g["action"].values); n = len(g)
    epi = pd.concat([pd.read_parquet(f) for f in glob.glob(D + ds + "/meta/episodes/**/*.parquet", recursive=True)])
    row = epi[epi.episode_index == ep].iloc[0]
    F = {k: frames(ds, row, k, n) for k in CAMS}
    pol.reset(); P = []
    for t in range(n):
        obs = {"observation.state": torch.tensor(S[t], dtype=torch.float32), **{f"observation.images.{k}": torch.from_numpy(F[k][min(t, len(F[k]) - 1)]).permute(2, 0, 1).float() / 255 for k in CAMS}}
        t1 = time.perf_counter()
        with torch.inference_mode(): a = post(pol.select_action(pre(obs))).squeeze(0).numpy()
        if t % 100 == 0: tinf.append(time.perf_counter() - t1)
        P.append(a)
    P = np.array(P)
    cmd = S[0].astype(float).copy(); y = cmd[:5].copy(); out, clipped, capped = [], 0, 0
    for a in P:
        y = y + 0.3 * (a[:5] - y); gg = np.concatenate([np.clip(y, lo, hi), a[5:]]); clipped += int((gg[:5] != y).sum())
        d = np.clip(gg - cmd, -3, 3); capped += int((d != gg - cmd).sum()); cmd = cmd + d; out.append(cmd.copy())
    out = np.array(out); raw_steps = np.abs(np.diff(P, axis=0)); st = np.abs(np.diff(out, axis=0))
    b = [i - 1 for i in range(100, n, 100)]
    wr = (P[:, 4] + 100) / 200 * 4095
    results[f"{ds.split('_', 3)[-1]}_ep{ep}"] = {
        "frames": n, "mae_vs_recorded": np.abs(P - A).mean(0).round(2).tolist(),
        "first_cmd_minus_state": (P[0] - S[0]).round(2).tolist(),
        "policy_boundary_jump_max": raw_steps[b].max(0).round(2).tolist() if b else None,
        "policy_inner_step_max": np.delete(raw_steps, b, 0).max(0).round(2).tolist(),
        "sent_step_max": st.max(0).round(2).tolist(), "joint_limit_clips": clipped, "step_cap_hits": capped,
        "wrist_raw_range": [int(wr.min()), int(wr.max())], "wrist_pred_jump_max": round(float(raw_steps[:, 4].max()), 2),
        "gripper_pred_range": [round(float(P[:, 5].min()), 1), round(float(P[:, 5].max()), 1)], "gripper_rec_range": [round(float(A[:, 5].min()), 1), round(float(A[:, 5].max()), 1)]}
    print(ds, ep, json.dumps(results[f"{ds.split('_', 3)[-1]}_ep{ep}"]), flush=True)
results["_chunk_inference_s"] = {"p50": round(float(np.median(tinf)), 3), "max": round(float(max(tinf)), 3), "n": len(tinf)}
results["_joint_limits_norm"] = {"lo": lo.round(1).tolist(), "hi": hi.round(1).tolist()}
json.dump(results, open(K + "/offline_dryrun.json", "w"), indent=1); print(json.dumps(results["_chunk_inference_s"]))
