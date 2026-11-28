"""Read-only re-verification of the _wristfix copies against the originals."""
import glob, json, os, sys
import numpy as np, pyarrow as pa, pyarrow.parquet as pq

sys.path.insert(0, "/home/purple/lerobot/src")
from lerobot.datasets.compute_stats import aggregate_feature_stats, get_feature_stats  # noqa: E402

TURN = 200.0 * 4096 / 4095
WR = 4
QK = ["min", "max", "mean", "std", "count", "q01", "q10", "q50", "q90", "q99"]
wrap = lambda x: (np.asarray(x) + TURN / 2) % TURN - TURN / 2


def load(root):
    t = pa.concat_tables([pq.read_table(f) for f in sorted(glob.glob(root + "/data/*/*.parquet"))]).to_pandas()
    return t.sort_values("index").reset_index(drop=True)


def ep_meta(root):
    return pa.concat_tables([pq.read_table(f) for f in sorted(glob.glob(root + "/meta/episodes/*/*.parquet"))]).to_pandas()


man = json.load(open(sys.argv[1]))
rows = []
for d in man["datasets"]:
    src, dst = d["source"], d["copy"]
    o, c = load(src), load(dst)
    r = {"name": os.path.basename(dst)}
    # identical columns / files
    r["rows"] = len(c)
    r["non-action columns identical"] = all(
        (np.stack(o[k]) == np.stack(c[k])).all() if o[k].dtype == object else (o[k].to_numpy() == c[k].to_numpy()).all()
        for k in o.columns if k != "action")
    ao, ac, st = np.stack(o["action"]), np.stack(c["action"]), np.stack(c["observation.state"])
    r["other 5 action joints identical"] = bool(np.array_equal(np.delete(ao, WR, 1), np.delete(ac, WR, 1)))
    r["videos/info/tasks identical (sha256)"] = all(
        d["sha256_source"][k] == d["sha256_copy"][k] for k in d["sha256_copy"] if k.startswith(("videos/", "meta/info", "meta/tasks")))
    r["changed files"] = d["files_changed"]
    ep = c["episode_index"].to_numpy()
    same = np.diff(ep) == 0
    # wrist metrics before / after
    for tag, a in (("before", ao), ("after", ac)):
        e = np.abs(a[:, WR] - st[:, WR])
        r[f"{tag} |a-s| med/p95/max"] = [round(float(np.median(e)), 2), round(float(np.percentile(e, 95)), 2), round(float(e.max()), 2)]
        r[f"{tag} jumps>50"] = int(np.sum((np.abs(np.diff(a[:, WR])) > 50) & same))
        r[f"{tag} max |da|"] = round(float(np.max(np.abs(np.diff(a[:, WR]))[same])), 2)
    # continuity of the corrected wrist action vs the other joints' actions (per-frame step, p99)
    r["after wrist step p99 / other joints p99"] = [round(float(np.percentile(np.abs(np.diff(ac[:, WR]))[same], 99)), 2),
                                                   round(float(np.percentile(np.abs(np.diff(np.delete(ac, WR, 1), axis=0))[same], 99)), 2)]
    r["after action range"] = [round(float(ac[:, WR].min()), 1), round(float(ac[:, WR].max()), 1)]
    # stats consistency: recompute from the COPY's data and compare to the COPY's stored stats (all 6 joints)
    em = ep_meta(dst)
    worst_ep = 0.0
    per = []
    for _, row in em.iterrows():
        e = int(row["episode_index"])
        s = get_feature_stats(ac[ep == e], axis=0, keepdims=False)
        per.append({k: np.asarray(v, dtype=np.float64) for k, v in s.items()})
        for k in QK:
            worst_ep = max(worst_ep, float(np.max(np.abs(np.asarray(row[f"stats/action/{k}"], dtype=np.float64) - per[-1][k]))))
    stored = json.load(open(dst + "/meta/stats.json"))["action"]
    agg = aggregate_feature_stats(per)
    worst_ds = max(float(np.max(np.abs(np.asarray(stored[k], dtype=np.float64) - np.asarray(agg[k], dtype=np.float64)))) for k in QK)
    r["stats match recomputed (episode / stats.json max diff)"] = [worst_ep, round(worst_ds, 7)]
    # stats.json: only action[wrist_roll] differs from the original
    so = json.load(open(src + "/meta/stats.json"))
    diff_keys = []
    for feat in so:
        for k in so[feat]:
            a, b = np.asarray(so[feat][k], dtype=np.float64), np.asarray(stored[k] if feat == "action" else json.load(open(dst + "/meta/stats.json"))[feat][k], dtype=np.float64)
            if not np.array_equal(a, b):
                idx = np.argwhere(a != b).ravel().tolist() if a.ndim == 1 else "all"
                diff_keys.append(f"{feat}.{k}{idx}")
    r["stats.json differences"] = sorted(set(x.split(".")[0] + ":" + x.split("[")[1] if "[" in x else x for x in diff_keys))
    rows.append(r)

# LeRobot can open every copy (read only)
from lerobot.datasets.lerobot_dataset import LeRobotDataset  # noqa: E402
for r in rows:
    root = f"/home/purple/omx_datasets/{r['name']}"
    ds = LeRobotDataset(repo_id=f"local/{r['name']}", root=root, download_videos=False)
    item = ds[len(ds) // 2]
    r["LeRobotDataset load"] = f"ok: {ds.num_episodes} ep, {ds.num_frames} frames, sample keys {len(item)}"
print(json.dumps(rows, ensure_ascii=False, indent=1, default=str))
