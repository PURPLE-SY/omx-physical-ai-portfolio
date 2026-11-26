#!/usr/bin/env python3
"""Episode/frame inventory of every LeRobot dataset (meta/info.json) under the given roots. Read only.
Written 2026-11-27 for this portfolio (inventory -> docs/dataset-inventory.csv)."""
import os, json, glob, subprocess, csv, sys
roots = sys.argv[1:] or [os.path.expanduser("~/omx_datasets")]
rows = []
for root in roots:
    for info in glob.glob(root + "/**/meta/info.json", recursive=True):
        d = os.path.dirname(os.path.dirname(info))
        i = json.load(open(info))
        rows.append(dict(path=os.path.relpath(d, root), episodes=i.get("total_episodes"), frames=i.get("total_frames"),
                         fps=i.get("fps"), robot=i.get("robot_type"),
                         cams="|".join(k.split(".")[-1] for k in i.get("features", {}) if "images" in k),
                         files=sum(len(f) for _, _, f in os.walk(d)),
                         bytes=int(subprocess.run(["du", "-sb", d], capture_output=True, text=True).stdout.split()[0])))
w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0])); w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["path"]))
