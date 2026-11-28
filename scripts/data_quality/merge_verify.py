"""Read-only check that the merged dataset equals its six sources, episode by episode."""
import glob, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pyarrow as pa, pyarrow.parquet as pq

sys.path.insert(0, "/home/purple/lerobot/src")
from lerobot.datasets.compute_stats import aggregate_feature_stats, get_feature_stats  # noqa: E402

R = "/home/purple/omx_datasets"
M = f"{R}/pick_place_LF02_11_21_wristfix_merged"
SRC = [f"{R}/pick_place_Left_11_21_F02_S0{i}_wristfix" for i in range(1, 7)]
CAMS = ["bottom", "wrist", "top"]
QK = ["min", "max", "mean", "std", "count", "q01", "q10", "q50", "q90", "q99"]
res = {"problems": []}
P = res["problems"]


def data(root):
    t = pa.concat_tables([pq.read_table(f) for f in sorted(glob.glob(root + "/data/*/*.parquet"))]).to_pandas()
    return t.sort_values("index").reset_index(drop=True)


def eps(root):
    t = pa.concat_tables([pq.read_table(f) for f in sorted(glob.glob(root + "/meta/episodes/*/*.parquet"))]).to_pandas()
    return t.sort_values("episode_index").reset_index(drop=True)


def framemd5(path):
    out = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-map", "0:v:0", "-f", "framemd5", "-"],
                         capture_output=True, text=True, check=True).stdout
    tbm = re.search(r"#tb 0: (\d+)/(\d+)", out)
    tbv = int(tbm.group(1)) / int(tbm.group(2))
    rows = [l.split(",") for l in out.splitlines() if l and not l.startswith("#")]
    return [(int(r[2]) * tbv, r[5].strip()) for r in rows]  # (pts seconds, md5)


md, me = data(M), eps(M)
info = json.load(open(M + "/meta/info.json"))
fps = info["fps"]
res["merged"] = {"episodes": info["total_episodes"], "frames": info["total_frames"], "rows": len(md),
                 "meta_episodes": len(me), "tasks": info.get("total_tasks"), "fps": fps,
                 "features": sorted(info["features"])}
if (info["total_episodes"], info["total_frames"], len(md), len(me)) != (60, 35748, 35748, 60):
    P.append("counts differ from 60 / 35748")
if not np.array_equal(md["index"].to_numpy(), np.arange(len(md))): P.append("index not continuous")
if not np.array_equal(me["episode_index"].to_numpy(), np.arange(60)): P.append("episode_index not 0..59")

# ---- frame data: merged episode k == source episode, all columns except index/episode_index (renumbered)
k = 0
src_ep_stats, mapping = [], []
for si, s in enumerate(SRC):
    sd, se = data(s), eps(s)
    for _, srow in se.iterrows():
        e = int(srow["episode_index"])
        a = sd[sd["episode_index"] == e].reset_index(drop=True)
        b = md[md["episode_index"] == k].reset_index(drop=True)
        mrow = me.iloc[k]
        mapping.append((os.path.basename(s), e, k))
        if len(a) != len(b) or int(mrow["length"]) != len(a): P.append(f"ep{k}: length differs")
        for col in ["observation.state", "action"]:
            if not np.array_equal(np.stack(a[col]), np.stack(b[col])): P.append(f"ep{k}: {col} differs from source")
        for col in ["timestamp", "frame_index", "task_index"]:
            if not np.array_equal(a[col].to_numpy(), b[col].to_numpy()): P.append(f"ep{k}: {col} differs")
        if int(mrow["dataset_from_index"]) != int(b["index"].min()) or int(mrow["dataset_to_index"]) != int(b["index"].max()) + 1:
            P.append(f"ep{k}: dataset_from/to_index wrong")
        # per-episode stats copied unchanged
        for feat in ["action", "observation.state"] + [f"observation.images.{c}" for c in CAMS]:
            for q in QK:
                x = np.asarray(srow[f"stats/{feat}/{q}"].tolist() if hasattr(srow[f"stats/{feat}/{q}"], "tolist") else srow[f"stats/{feat}/{q}"], dtype=object)
                y = mrow[f"stats/{feat}/{q}"]
                if not np.allclose(np.array(np.stack(x) if x.dtype == object and x.ndim and hasattr(x[0], '__len__') else x, dtype=float),
                                   np.array(np.stack(y) if hasattr(y[0], '__len__') else y, dtype=float)):
                    P.append(f"ep{k}: episode stats {feat}/{q} differ")
        k += 1
res["episode_mapping"] = mapping

# ---- videos: decoded frame md5 of every episode segment, merged vs source (all three cameras)
def seg_hashes(root, row, cam):
    ci, fi = int(row[f"videos/observation.images.{cam}/chunk_index"]), int(row[f"videos/observation.images.{cam}/file_index"])
    a, b = float(row[f"videos/observation.images.{cam}/from_timestamp"]), float(row[f"videos/observation.images.{cam}/to_timestamp"])
    path = f"{root}/videos/observation.images.{cam}/chunk-{ci:03d}/file-{fi:03d}.mp4"
    return path, a, b

cache = {}
def hashes(path):
    if path not in cache:
        cache[path] = framemd5(path)
    return cache[path]

paths = set()
for root, table in [(M, me)] + [(s, eps(s)) for s in SRC]:
    for _, row in table.iterrows():
        for c in CAMS:
            paths.add(seg_hashes(root, row, c)[0])
with ThreadPoolExecutor(6) as ex:
    for p, h in zip(sorted(paths), ex.map(framemd5, sorted(paths))):
        cache[p] = h

def tb(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=time_base",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout.strip()
    n, d = out.split("/")
    return int(n) / int(d)

tbs = {p: tb(p) for p in cache}
def seg_md5(root, row, cam):
    path, a, b = seg_hashes(root, row, cam)
    return [m for pts, m in cache[path] if a - 1e-4 <= pts < b - 1e-4]

video_frames = {c: 0 for c in CAMS}
k = 0
for s in SRC:
    for _, srow in eps(s).iterrows():
        mrow = me.iloc[k]
        for c in CAMS:
            x, y = seg_md5(s, srow, c), seg_md5(M, mrow, c)
            video_frames[c] += len(y)
            if len(y) != int(mrow["length"]): P.append(f"ep{k} {c}: {len(y)} video frames != {int(mrow['length'])}")
            if x != y: P.append(f"ep{k} {c}: decoded frames differ from source ({sum(i != j for i, j in zip(x, y))} of {len(y)})")
        k += 1
res["video_frames_per_camera"] = video_frames
res["video_files"] = {os.path.relpath(p, M): len(cache[p]) for p in sorted(cache) if p.startswith(M)}

# ---- dataset stats.json: equals aggregation of the 60 episode stats, and state/action equal a fresh computation
stored = json.load(open(M + "/meta/stats.json"))
worst = {}
for feat in ["action", "observation.state"] + [f"observation.images.{c}" for c in CAMS]:
    per = []
    for _, row in me.iterrows():
        per.append({q: np.array(np.stack(row[f"stats/{feat}/{q}"]) if hasattr(row[f"stats/{feat}/{q}"][0], "__len__") else row[f"stats/{feat}/{q}"], dtype=float)
                    if not isinstance(row[f"stats/{feat}/{q}"][0], np.ndarray) or True else None for q in QK})
    def deep(v):
        v = np.asarray(v, dtype=object)
        while v.dtype == object:
            v = np.stack([deep(x) for x in v]) if v.ndim else np.asarray(v.item(), dtype=float)
        return v.astype(float)
    per = [{q: deep(row[f"stats/{feat}/{q}"]) for q in QK} for _, row in me.iterrows()]
    agg = aggregate_feature_stats(per)
    worst[feat] = max(float(np.max(np.abs(np.asarray(stored[feat][q], dtype=float).reshape(-1) - np.asarray(agg[q], dtype=float).reshape(-1)))) for q in QK)
    if feat in ("action", "observation.state"):
        arr = np.stack(md[feat])
        fresh = aggregate_feature_stats([{q: np.asarray(v, dtype=float) for q, v in get_feature_stats(arr[md["episode_index"].to_numpy() == e], axis=0, keepdims=False).items()} for e in range(60)])
        worst[feat + " (fresh from data)"] = max(float(np.max(np.abs(np.asarray(stored[feat][q], dtype=float) - fresh[q]))) for q in QK)
res["stats_max_abs_diff"] = worst
if max(worst.values()) > 1e-4: P.append(f"stats mismatch {worst}")

# ---- wrist_roll after merge
st, ac, ep = np.stack(md["observation.state"]), np.stack(md["action"]), md["episode_index"].to_numpy()
same = np.diff(ep) == 0
e = np.abs(ac[:, 4] - st[:, 4])
res["wrist_roll"] = {"|a-s| med/p95/max": [round(float(np.median(e)), 2), round(float(np.percentile(e, 95)), 2), round(float(e.max()), 2)],
                     "jumps>50": int(np.sum((np.abs(np.diff(ac[:, 4])) > 50) & same)),
                     "action range": [round(float(ac[:, 4].min()), 1), round(float(ac[:, 4].max()), 1)],
                     "state range": [round(float(st[:, 4].min()), 1), round(float(st[:, 4].max()), 1)]}

from lerobot.datasets.lerobot_dataset import LeRobotDataset  # noqa: E402
ds = LeRobotDataset("Purple-SY/pick_place_LF02_11_21_wristfix_merged", root=M, download_videos=False)
items = [ds[i] for i in (0, len(ds) // 2, len(ds) - 1)]
res["LeRobotDataset"] = {"episodes": ds.num_episodes, "frames": ds.num_frames,
                         "image shapes": {k: list(v.shape) for k, v in items[1].items() if "images" in k}}
res["problems_count"] = len(P)
res["problems"] = P[:30]
print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
