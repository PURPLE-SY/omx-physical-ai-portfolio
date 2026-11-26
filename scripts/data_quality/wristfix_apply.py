"""Make <dataset>_wristfix copies of pick_place_Left_11_21_F02_S01..S06 with action[wrist_roll] corrected (method A:
fold(action + job offset)). The originals are only read. Changed in the copy: data/*.parquet (action column, wrist_roll
element only), meta/episodes/*.parquet (stats/action/*, wrist_roll element only), meta/stats.json (action, wrist_roll
element only). Everything else is a byte copy. Writes a manifest (SHA256 + diff summary) next to this script.

usage: python wristfix_apply.py <manifest_out.json>     (run with the lerobot venv; cwd = this scratchpad)
"""
import hashlib, json, os, shutil, sys
import numpy as np, pyarrow as pa, pyarrow.parquet as pq

sys.path.insert(0, "/home/purple/lerobot/src")
from lerobot.datasets.compute_stats import aggregate_feature_stats, get_feature_stats  # noqa: E402

ROOT = "/home/purple/omx_datasets"
TURN = 200.0 * 4096 / 4095
WR = 4
QKEYS = ["min", "max", "mean", "std", "count", "q01", "q10", "q50", "q90", "q99"]
# job -> episodes (S05 was recorded in two app runs: record ep0-2, resume ep3-9)
JOBS = {1: [range(0, 10)], 2: [range(0, 10)], 3: [range(0, 10)], 4: [range(0, 10)],
        5: [range(0, 3), range(3, 10)], 6: [range(0, 10)]}
# offsets from the read-only simulation (wrist_sim.py); re-estimated below and must agree within 0.05
EXPECTED = {(1, 0): 53.97, (2, 0): 55.34, (3, 0): 54.26, (4, 0): 51.92, (5, 0): 54.60, (5, 3): 51.38, (6, 0): 51.48}


def wrap(x):
    return (np.asarray(x) + TURN / 2) % TURN - TURN / 2


def fold(x):
    return (np.asarray(x) + 100) % TURN - 100


def circ_median(d):
    ang = d / TURN * 2 * np.pi
    m = np.angle(np.mean(np.exp(1j * ang))) / (2 * np.pi) * TURN
    return float(m + np.median(wrap(d - m)))


def estimate_offset(st, ac):
    v = np.abs(wrap(np.diff(ac[:, WR], prepend=ac[0, WR])))
    still = v < 0.2
    return circ_median(st[still, WR] - ac[still, WR])


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tree_hashes(root):
    out = {}
    for r, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, root)] = sha256(p)
    return dict(sorted(out.items()))


def files(root, sub):
    d = os.path.join(root, sub)
    return sorted(os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs if f.endswith(".parquet"))


def as_np(stats):
    return {k: np.asarray(v, dtype=np.float64) for k, v in stats.items()}


def main(manifest_path):
    manifest = {"method": "A: action[wrist_roll] = fold(action[wrist_roll] + job_offset) into [-100,100]",
                "turn_units": TURN, "datasets": []}
    for i, parts in JOBS.items():
        src = f"{ROOT}/pick_place_Left_11_21_F02_S0{i}"
        dst = src + "_wristfix"
        if os.path.exists(dst):
            raise SystemExit(f"refusing: {dst} already exists")
        src_hash_before = tree_hashes(src)
        info = json.load(open(f"{src}/meta/info.json"))
        assert info["features"]["action"]["names"][WR] == "wrist_roll.pos"

        # --- read all frames of the original (for offsets and stats)
        data_files = files(src, "data")
        tables = [pq.read_table(f) for f in data_files]
        allt = pa.concat_tables(tables).to_pandas()
        st_all, ac_all, ep_all = np.stack(allt["observation.state"]), np.stack(allt["action"]), allt["episode_index"].to_numpy()
        ep_offset = {}
        job_rec = []
        for p in parts:
            sel = np.isin(ep_all, list(p))
            o = estimate_offset(st_all[sel], ac_all[sel])
            exp = EXPECTED[(i, p.start)]
            if abs(o - exp) > 0.05:
                raise SystemExit(f"S0{i} ep{p.start}-{p.stop-1}: offset {o:.3f} != expected {exp}")
            for e in p:
                ep_offset[e] = o
            job_rec.append({"episodes": f"{p.start}-{p.stop-1}", "offset_units": round(o, 4),
                            "offset_counts": round(o * 4095 / 200, 1), "offset_deg": round(o * 360 / TURN, 2)})
        assert set(ep_offset) == set(np.unique(ep_all).tolist())

        # --- copy (byte copy of everything; then the three kinds of files are rewritten)
        shutil.copytree(src, dst, copy_function=shutil.copy2)
        changes = []

        # data parquet: rewrite the action column only, keep schema, metadata and row groups
        for f in data_files:
            pf = pq.ParquetFile(f)
            rel = os.path.relpath(f, src)
            out = os.path.join(dst, rel)
            schema = pf.schema_arrow
            comp = pf.metadata.row_group(0).column(0).compression
            n_changed = 0
            max_wr = 0.0
            with pq.ParquetWriter(out, schema, compression=comp) as w:
                for g in range(pf.num_row_groups):
                    t = pf.read_row_group(g)
                    act = np.stack(t.column("action").to_numpy(zero_copy_only=False)).astype(np.float32)
                    eps = t.column("episode_index").to_numpy()
                    new = act.copy()
                    off = np.array([ep_offset[int(e)] for e in eps])
                    new[:, WR] = fold(act[:, WR].astype(np.float64) + off).astype(np.float32)
                    assert np.array_equal(new[:, :WR], act[:, :WR]) and np.array_equal(new[:, WR + 1:], act[:, WR + 1:])
                    n_changed += int(np.sum(new[:, WR] != act[:, WR]))
                    max_wr = max(max_wr, float(np.max(np.abs(new[:, WR] - act[:, WR]))))
                    typ = schema.field("action").type
                    col = pa.FixedSizeListArray.from_arrays(pa.array(new.reshape(-1), type=typ.value_type), typ.list_size)
                    t = t.set_column(t.schema.get_field_index("action"), schema.field("action"), col)
                    w.write_table(t.cast(schema))
            changes.append({"file": rel, "what": "action[:, wrist_roll]", "rows_changed": n_changed,
                            "max_abs_change": round(max_wr, 3), "other_columns": "identical (asserted)"})

        # --- recompute action stats with LeRobot's own functions (fixed action), per episode
        new_all = ac_all.copy()
        new_all[:, WR] = fold(ac_all[:, WR].astype(np.float64) + np.array([ep_offset[int(e)] for e in ep_all])).astype(np.float32)

        ep_files = files(src, "meta/episodes")
        per_ep_new = {}
        repro = {"episode_stats_orig_max_abs_diff": 0.0}
        for e in np.unique(ep_all):
            m = ep_all == e
            per_ep_new[int(e)] = as_np(get_feature_stats(new_all[m], axis=0, keepdims=False))
        for f in ep_files:
            rel = os.path.relpath(f, src)
            t = pq.read_table(f)
            eps = t.column("episode_index").to_pylist()
            for k in QKEYS:
                name = f"stats/action/{k}"
                old = [np.asarray(v, dtype=np.float64) for v in t.column(name).to_pylist()]
                newv = []
                for e, o in zip(eps, old):
                    # reproduction check on the ORIGINAL action: LeRobot's function must give the stored stats
                    ref = as_np(get_feature_stats(ac_all[ep_all == e], axis=0, keepdims=False))[k]
                    repro["episode_stats_orig_max_abs_diff"] = max(repro["episode_stats_orig_max_abs_diff"],
                                                                    float(np.max(np.abs(ref - o))))
                    v = o.copy()
                    if k != "count":
                        v[WR] = per_ep_new[e][k][WR]
                    newv.append(v.astype(np.float64).tolist())
                typ = t.schema.field(name).type
                t = t.set_column(t.schema.get_field_index(name), t.schema.field(name), pa.array(newv, type=typ))
            pf = pq.ParquetFile(f)
            pq.write_table(t, os.path.join(dst, rel), compression=pf.metadata.row_group(0).column(0).compression)
            changes.append({"file": rel, "what": "stats/action/{min,max,mean,std,q01..q99}[wrist_roll] per episode"})

        # --- dataset stats.json: aggregate the per-episode action stats like LeRobot does, replace wrist_roll only
        stats = json.load(open(f"{src}/meta/stats.json"))
        orig_eps = [as_np(get_feature_stats(ac_all[ep_all == e], axis=0, keepdims=False)) for e in sorted(per_ep_new)]
        agg_orig = aggregate_feature_stats(orig_eps)
        repro["stats_json_orig_max_abs_diff"] = max(float(np.max(np.abs(np.asarray(agg_orig[k], dtype=np.float64)
                                                                          - np.asarray(stats["action"][k], dtype=np.float64))))
                                                     for k in QKEYS)
        agg_new = aggregate_feature_stats([per_ep_new[e] for e in sorted(per_ep_new)])
        before_wr = {k: stats["action"][k][WR] for k in QKEYS if k != "count"}
        for k in QKEYS:
            if k == "count":
                continue
            stats["action"][k][WR] = float(np.asarray(agg_new[k])[WR])
        with open(f"{dst}/meta/stats.json", "w") as fh:
            json.dump(stats, fh, indent=4)
        changes.append({"file": "meta/stats.json", "what": "action.{min,max,mean,std,q..}[wrist_roll]",
                        "before": {k: round(v, 3) for k, v in before_wr.items()},
                        "after": {k: round(stats["action"][k][WR], 3) for k in before_wr}})

        src_hash_after = tree_hashes(src)
        dst_hash = tree_hashes(dst)
        manifest["datasets"].append({
            "source": src, "copy": dst, "jobs": job_rec, "reproduction_check_on_original": repro,
            "source_unchanged": src_hash_before == src_hash_after,
            "files_identical": [k for k in dst_hash if src_hash_before.get(k) == dst_hash[k]],
            "files_changed": [k for k in dst_hash if src_hash_before.get(k) != dst_hash[k]],
            "sha256_source": src_hash_before, "sha256_copy": dst_hash, "changes": changes})
        print(f"S0{i}: done, changed {len(manifest['datasets'][-1]['files_changed'])} files, source unchanged "
              f"{src_hash_before == src_hash_after}, repro {repro}", flush=True)
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1])
