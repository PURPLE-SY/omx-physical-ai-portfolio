"""Build the GitHub Pages video player (video/index.html) from docs/videos.md.

Uses only files already in assets/media/. Run from the repository root:
    python tools/make_player.py
"""
import json, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
md = (ROOT / "docs/videos.md").read_text(encoding="utf-8")

CATS = {"🟢": ("act", "ACT 자율 구동 — 성공"), "🔵": ("replay", "녹화 리플레이 — 성공 (정책 아님)"),
        "🟡": ("partial", "부분 성공"), "🔴": ("fail", "실패"), "🟣": ("teleop", "텔레오퍼레이션 시연 (자율 구동 아님)")}
items, cat = [], None
for block in re.split(r"\n(?=##+ )", md):
    head = block.split("\n", 1)[0]
    if head.startswith("## "):
        cat = next((v for k, v in CATS.items() if k in head), None)
        continue
    m = re.match(r"### (\d\d) · (.+)", head)
    if not (m and cat):
        continue
    num, title = m.groups()
    vid = re.search(r'href="\.\./assets/media/videos/([^"]+\.mp4)"', block).group(1)
    thumb = re.search(r'src="\.\./assets/media/thumbs/([^"]+\.jpg)"', block).group(1)
    facts = []
    for k, v in re.findall(r"^- \*\*(.+?):\*\* (.+)$", block, re.M):
        v = re.sub(r"`([^`]+)`", r"\1", v).replace("**", "")
        facts.append([k, v])
    items.append({"id": num, "title": title, "cat": cat[0], "catLabel": cat[1],
                  "video": f"../assets/media/videos/{vid}", "thumb": f"../assets/media/thumbs/{thumb}", "facts": facts})

assert len(items) == len(list((ROOT / "assets/media/videos").glob("*.mp4"))), len(items)
for it in items:
    assert (ROOT / "video" / it["video"]).resolve().exists() and (ROOT / "video" / it["thumb"]).resolve().exists(), it["id"]

page = (ROOT / "tools/player_template.html").read_text(encoding="utf-8")
page = page.replace("/*__DATA__*/[]", json.dumps(items, ensure_ascii=False))
(ROOT / "video").mkdir(exist_ok=True)
(ROOT / "video/index.html").write_text(page, encoding="utf-8")
print(len(items), "videos")
