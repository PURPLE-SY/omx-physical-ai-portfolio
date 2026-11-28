import json, glob
import av, numpy as np, pandas as pd, torch
K = "/home/purple/omx_logs/b-f01-act-run-20261126"; W = "/home/purple/omx_models/omx-act-arm-b-f01-best12000-cpu-compat"; D = "/home/purple/omx_datasets/"
lim = json.load(open(K + "/safety-1d2d-132a.lf01-run.json"))["joint_limits"]
J = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll"]
lo = np.array([lim[j][0] / 4095 * 200 - 100 for j in J]); hi = np.array([lim[j][1] / 4095 * 200 - 100 for j in J])
def policy():
    from lerobot.configs.policies import PreTrainedConfig
    from lerobot.policies.act.modeling_act import ACTPolicy
    from lerobot.policies.factory import make_pre_post_processors
    torch.set_num_threads(4)
    cfg = PreTrainedConfig.from_pretrained(W); pol = ACTPolicy.from_pretrained(W, config=cfg).eval()
    pre, post = make_pre_post_processors(cfg, pretrained_path=W, preprocessor_overrides={"device_processor": {"device": "cpu"}})
    return pol, pre, post
def load_episode(ds, ep):
    df = pd.concat([pd.read_parquet(f) for f in glob.glob(D + ds + "/data/**/*.parquet", recursive=True)])
    g = df[df.episode_index == ep].sort_values("frame_index"); n = len(g)
    epi = pd.concat([pd.read_parquet(f) for f in glob.glob(D + ds + "/meta/episodes/**/*.parquet", recursive=True)])
    row = epi[epi.episode_index == ep].iloc[0]; info = json.load(open(D + ds + "/meta/info.json")); F = {}
    for key in ("bottom", "wrist", "top"):
        k = f"observation.images.{key}"
        path = D + ds + "/" + info["video_path"].format(video_key=k, chunk_index=int(row[f"videos/{k}/chunk_index"]), file_index=int(row[f"videos/{k}/file_index"]))
        t0 = float(row[f"videos/{k}/from_timestamp"]); out = []
        with av.open(path) as c:
            for fr in c.decode(video=0):
                if fr.time >= t0 - 1e-3:
                    out.append(fr.to_ndarray(format="rgb24"))
                    if len(out) == n: break
        F[key] = out
    return np.stack(g["observation.state"].values), np.stack(g["action"].values), F
