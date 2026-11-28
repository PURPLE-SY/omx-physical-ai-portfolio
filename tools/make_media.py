"""Make portfolio media copies (originals are never modified).

- assets/media/videos/: H.264 copies of representative runs (portfolio_videos already H.264 -> copied;
  failure/collision examples re-encoded to H.264, 640 px, no audio)
- assets/media/thumbs/: one JPEG per video (frame at 40 % of the run)
- assets/media/evidence/multiview_*.jpg: top / bottom(side) / wrist frames from the same replay instant
Usage: python tools/make_media.py <src_light> <src_backup>
"""
import sys, shutil, json, hashlib
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

LIGHT, BACK = Path(sys.argv[1]), Path(sys.argv[2])
ROOT = Path(__file__).resolve().parents[1]
V, T, E = (ROOT / "assets/media" / d for d in ("videos", "thumbs", "evidence"))
for d in (V, T, E):
    d.mkdir(parents=True, exist_ok=True)
FONT = "/mnt/c/Windows/Fonts/malgun.ttf"

def frame_at(path, frac):
    c = av.open(str(path)); s = c.streams.video[0]
    n = s.frames or int(float(c.duration / 1e6) * float(s.average_rate))
    target = int(n * frac)
    for i, f in enumerate(c.decode(s)):
        if i >= target:
            img = f.to_image(); c.close(); return img
    c.close(); return img

def reencode(src, dst, width=640):
    i = av.open(str(src)); o = av.open(str(dst), "w")
    si = i.streams.video[0]
    so = o.add_stream("libx264", rate=si.average_rate or 30)
    h = int(si.height * width / si.width) // 2 * 2
    so.width, so.height, so.pix_fmt = width, h, "yuv420p"
    so.options = {"crf": "28", "preset": "medium", "movflags": "+faststart"}
    for f in i.decode(si):
        for p in so.encode(f.reformat(width=width, height=h, format="yuv420p")):
            o.mux(p)
    for p in so.encode():
        o.mux(p)
    o.close(); i.close()

manifest = []
# 2026-11-28: F03 S02 replays re-judged as partial success (placement precision)
RENAME = {"07_B-F03-S02_REPLAY_success_20261127-2054": "07_B-F03-S02_REPLAY_partial_20261127-2054",
          "08_B-F03-S02_REPLAY_success_20261127-2057": "08_B-F03-S02_REPLAY_partial_20261127-2057"}
PV = BACK / "01_reports_docs/omx_reports/final_20261128/portfolio_videos"
for mp4 in sorted(PV.glob("*.mp4")):
    stem = RENAME.get(mp4.stem, mp4.stem)
    shutil.copy2(mp4, V / f"{stem}.mp4")
    shutil.copy2(mp4.with_suffix(".jpg"), T / f"{stem}.jpg")
    manifest.append({"file": f"{stem}.mp4", "origin": f"final_20261128/portfolio_videos/{mp4.name}", "processing": "copy"})

VC = BACK / "12_videos"
FAILS = {
    "10_B-F02-S05_ACT_collision_20261127-0022": VC / "2_partial_or_collision/omx-act-arm-b-f02-wristfix-best12000-cpu-compat_20261127-002248_ep1.mp4",
    "11_B-F02-S05_ACT_fail_collision_20261127-0037": VC / "3_fail/omx-act-arm-b-f02-wristfix-best12000-cpu-compat_20261127-003713_ep2.mp4",
    "12_B-F01-S03_ACT_partial_drag_20261126-2356": VC / "2_partial_or_collision/omx-act-arm-b-f01-best12000-cpu-compat-camwarp_20261126-235617_ep1.mp4",
    "13_B-F01-S03_ACT_fail_grasp_20261127-0001": VC / "3_fail/omx-act-arm-b-f01-best12000-cpu-compat-camwarp_20261127-000100_ep1.mp4",
}
for name, src in FAILS.items():
    if not src.exists():
        alt = list(VC.rglob(src.name)) + list((LIGHT / "B_02_logs_light/omx_logs/topview").glob(src.name))
        if not alt:
            print("MISSING", src.name); continue
        src = alt[0]
    reencode(src, V / f"{name}.mp4")
    frame_at(V / f"{name}.mp4", 0.4).save(T / f"{name}.jpg", quality=85)
    manifest.append({"file": f"{name}.mp4", "origin": f"12_videos/{src.parent.name}/{src.name}", "processing": "H.264 re-encode 640px crf28"})

# multi-view stills from replay runs (same frame fraction in each camera)
font = ImageFont.truetype(FONT, 20)
RUNS = {"multiview_F03-S02_replay_20261127-2054": LIGHT / "B_02_logs_light/omx_logs/lf03_s02_replay_20261127/results/run_20261127-205451/video",
        "multiview_F01-S03_replay_20261128-0254": LIGHT / "B_02_logs_light/omx_logs/lf01_s03_replay_20261128/results/run_20261128-025441/video"}
for name, d in RUNS.items():
    if not d.exists():
        print("MISSING", d); continue
    tiles = []
    for cam, lab in (("top", "탑뷰 (RealSense)"), ("bottom", "사이드/정면 (USB)"), ("wrist", "손목 카메라")):
        im = frame_at(d / f"{cam}.mp4", 0.45).convert("RGB").resize((480, 360))
        dr = ImageDraw.Draw(im); dr.rectangle((0, 0, 230, 34), fill=(0, 0, 0)); dr.text((8, 5), lab, fill="white", font=font)
        tiles.append(im)
    canvas = Image.new("RGB", (480 * 3 + 8, 360), "white")
    for k, im in enumerate(tiles):
        canvas.paste(im, (k * 484, 0))
    canvas.save(E / f"{name}.jpg", quality=85)
    manifest.append({"file": f"{name}.jpg", "origin": str(d.relative_to(LIGHT)), "processing": "frame at 45 % of each camera"})

for m in manifest:
    p = (V if m["file"].endswith(".mp4") else (T if (T / m["file"]).exists() and "multiview" not in m["file"] else E)) / m["file"]
    m["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest(); m["bytes"] = p.stat().st_size
json.dump(manifest, open(ROOT / "assets/media/MEDIA_MANIFEST.json", "w"), ensure_ascii=False, indent=1)
print(len(manifest), "items")
