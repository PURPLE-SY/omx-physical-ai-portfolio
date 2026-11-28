"""Build portfolio graphs from recorded logs only.

Every figure is drawn from a file listed in SOURCES; nothing is simulated or
filled in. Run:
    python tools/make_graphs.py <src_light> <src_backup>
where the two folders are local copies of the external-HDD backup
(omx_act_1121 / omx_backup_20261127). Output: assets/graphs/*.png and
assets/graphs/graph_data.json (the exact numbers plotted).
"""
import csv, json, sys, collections
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

LIGHT, BACK = Path(sys.argv[1]), Path(sys.argv[2])
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "graphs"
OUT.mkdir(parents=True, exist_ok=True)

for f in ("/mnt/c/Windows/Fonts/malgun.ttf", "/mnt/c/Windows/Fonts/NotoSansKR-VF.ttf"):
    if Path(f).exists():
        font_manager.fontManager.addfont(f)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
        break
plt.rcParams.update({
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#999999", "axes.labelcolor": "#666666",
    "xtick.color": "#666666", "ytick.color": "#666666",
    "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.8,
    "axes.titlesize": 13, "axes.titleweight": "bold", "font.size": 10,
    "legend.frameon": False, "figure.dpi": 110, "savefig.bbox": "tight",
    "axes.unicode_minus": False, "axes.axisbelow": True,
})
SERIES = ["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17", "#6a4ce2"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X"]
GOOD, PART, BAD, GRAY = "#0aac23", "#fbb315", "#dc3c3d", "#bdbdbd"
INK2 = "#666666"

MODELS = ["omx-act-arm-a-f01-13k-1124", "omx-act-arm-a-f02-13k-1124", "omx-act-arm-a-f03-13k-1124",
          "omx-act-arm-a-ex-13k-1124", "omx-act-arm-b-f01-13k-1124",
          "omx-act-arm-b-f02-wristfix-13k-1124", "omx-act-arm-b-ex-13k-1124"]
LABEL = {m: m.replace("omx-act-arm-", "").replace("-13k-1124", "").upper().replace("-WRISTFIX", " wristfix")
         for m in MODELS}
MDIR = LIGHT / "B_11_models" / "omx_models"
LOGS = LIGHT / "B_02_logs_light" / "omx_logs"
REP = BACK / "01_reports_docs" / "omx_reports"
DATA, SOURCES = {}, {}


def note(fig, text):
    fig.text(0.0, -0.02, text, ha="left", va="top", fontsize=8, color=INK2, wrap=True)


def save(fig, name, src, cond):
    note(fig, f"조건: {cond}\n출처: {src}")
    fig.savefig(OUT / f"{name}.png", facecolor="white")
    plt.close(fig)
    SOURCES[name] = {"source": src, "condition": cond}


# ---------- 1-2. training / validation loss per checkpoint ----------
loss = {}
for m in MODELS:
    rows = list(csv.DictReader(open(MDIR / m / "checkpoint_losses.csv")))
    loss[m] = [(int(r["step"]), float(r["training_loss"]), float(r["validation_loss"])) for r in rows]
DATA["checkpoint_losses"] = {LABEL[m]: v for m, v in loss.items()}
for idx, (key, title, ylab) in enumerate([(1, "ACT Training Loss (체크포인트별)", "training loss"),
                                           (2, "ACT Validation Loss (held-out 에피소드)", "validation loss")]):
    fig, ax = plt.subplots(figsize=(9, 4.6))
    for i, m in enumerate(MODELS):
        xs = [s for s, *_ in loss[m]]; ys = [r[key] for r in loss[m]]
        ax.plot(xs, ys, color=SERIES[i], lw=2, marker=MARKERS[i], ms=5, label=LABEL[m])
    ax.set_title(title, loc="left"); ax.set_xlabel("학습 step"); ax.set_ylabel(ylab + " (무차원)")
    ax.legend(ncol=4, loc="upper right", fontsize=8.5)
    save(fig, f"0{idx+1}_{'training' if key == 1 else 'validation'}_loss",
         "omx_models/<모델>/checkpoint_losses.csv (13k 모델 7종, 학습 PC 기록)",
         "ACT, 13,000 step, 1,000 step마다 체크포인트; A=오른팔, B=왼팔, F0N=층, EX=분류 장소")

# ---------- 3. best vs final ----------
bf = {}
for m in MODELS:
    ev = json.load(open(MDIR / m / "evaluation.json"))
    vl = {s: v for s, _, v in loss[m]}
    bf[LABEL[m]] = {"best_step": ev["roles"]["best"], "best": vl[ev["roles"]["best"]],
                    "final_step": ev["roles"]["final"], "final": vl[ev["roles"]["final"]]}
DATA["best_vs_final"] = bf
fig, ax = plt.subplots(figsize=(9, 4.2))
names = list(bf); x = range(len(names)); w = 0.38
ax.bar([i - w/2 - 0.01 for i in x], [bf[n]["best"] for n in names], w, color=SERIES[0], label="Best (최저 val loss)")
ax.bar([i + w/2 + 0.01 for i in x], [bf[n]["final"] for n in names], w, color=GRAY, label="Final (13,000 step)")
for i, n in enumerate(names):
    ax.text(i - w/2, bf[n]["best"] + 0.004, f'{bf[n]["best"]:.3f}\n@{bf[n]["best_step"]//1000}k', ha="center", fontsize=7.5)
    ax.text(i + w/2, bf[n]["final"] + 0.004, f'{bf[n]["final"]:.3f}', ha="center", fontsize=7.5, color=INK2)
ax.set_xticks(list(x), names, fontsize=9); ax.set_ylabel("validation loss (무차원)"); ax.set_ylim(0, 0.42)
ax.set_title("Best vs Final 체크포인트 validation loss", loc="left"); ax.legend(loc="upper left", ncol=2)
save(fig, "03_best_vs_final", "omx_models/<모델>/evaluation.json roles + checkpoint_losses.csv",
     "같은 held-out 분할; Best와 Final이 같은 step이면 막대 높이가 같음. val loss는 실물 성공률이 아님")

# ---------- 4. per-joint offline MAE (B F02 wristfix, 7000 vs 12000) ----------
ev = json.load(open(MDIR / "omx-act-arm-b-f02-wristfix-13k-1124" / "evaluation.json"))["offline_action_metrics"]
joints = [j.replace(".pos", "") for j in ev["joint_names"]]
DATA["joint_mae_b_f02"] = {ck: {"first_mae": ev[ck]["first_mae"], "chunk_mae": ev[ck]["chunk_mae"],
                                "frames": ev[ck]["frames"]} for ck in ("007000", "012000")}
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
for ax, metric, ttl in zip(axes, ("first_mae", "chunk_mae"), ("첫 action 오차", "chunk(100 step) 평균 오차")):
    for k, (ck, col) in enumerate((("007000", GRAY), ("012000", SERIES[0]))):
        ax.bar([i + (k - 0.5) * 0.4 for i in range(6)], ev[ck][metric], 0.38, color=col,
               label=f"체크포인트 {int(ck)}")
    ax.set_xticks(range(6), joints, rotation=25, fontsize=8.5); ax.set_title(ttl, loc="left", fontsize=11)
axes[0].set_ylabel("|예측 - 녹화 action| 평균 (관절 단위*)"); axes[0].legend(loc="upper left")
fig.suptitle("관절별 예측값 vs 실제(녹화)값 오차 — B팔 F02 wristfix", x=0.06, y=1.04, ha="left", fontweight="bold")
save(fig, "04_joint_prediction_error",
     "omx-act-arm-b-f02-wristfix-13k-1124/evaluation.json offline_action_metrics",
     f"held-out ep 48–59, {ev['012000']['frames']:,} 프레임; *LeRobot 정규화 관절 단위(gripper 0–100). 오프라인, 실물 아님")

# ---------- 5-6. data collection (teleop originals) ----------
inv = [r for r in csv.DictReader(open(ROOT / "docs" / "dataset-inventory.csv")) if r["kind"] == "teleop"]
day = collections.OrderedDict()
for r in sorted(inv, key=lambda r: r["recording_date"]):
    day[r["recording_date"]] = day.get(r["recording_date"], 0) + int(r["episodes"])
cum, s = [], 0
for v in day.values():
    s += v; cum.append(s)
DATA["daily_episodes"] = {"daily": day, "cumulative": dict(zip(day, cum))}
fig, axes = plt.subplots(2, 1, figsize=(10, 5.6), sharex=True, gridspec_kw={"height_ratios": [1.2, 1]})
lab = [d[5:] for d in day]
axes[0].bar(lab, list(day.values()), color=SERIES[0], width=0.7)
for i, v in enumerate(day.values()):
    axes[0].text(i, v + 3, str(v), ha="center", fontsize=7.5)
axes[0].set_ylabel("에피소드 / 일"); axes[0].set_title("날짜별 텔레옵 녹화량과 누적 에피소드", loc="left")
axes[1].plot(lab, cum, color=SERIES[0], lw=2, marker="o", ms=4)
axes[1].text(len(cum) - 1, cum[-1] + 40, f"{cum[-1]:,} ep", ha="right", fontsize=9, fontweight="bold")
axes[1].set_ylabel("누적 에피소드"); axes[1].set_ylim(0, cum[-1] * 1.15)
plt.setp(axes[1].get_xticklabels(), rotation=45, fontsize=8)
save(fig, "05_daily_collection", "docs/dataset-inventory.csv (kind=teleop, 85 폴더)",
     "2026-10-29~11-25, 로컬·HF 중복 제외 원본만; 진단·파생·평가 기록 제외. 10/17~10/28 원본은 미확인으로 미포함")

def floor_of(f):
    if "EX" in f: return "EX"
    if "층 구분 이전" in f: return "1층(구분 전)"
    return f if f.endswith("층") else "기타"
cats = ["1층(구분 전)", "1층", "2층", "3층", "EX", "기타"]
arms = ["Left", "Right", "Front", "Both"]
dist = {a: {c: 0 for c in cats} for a in arms}
for r in inv:
    dist[r["arm"]][floor_of(r["floor"])] += int(r["episodes"])
DATA["arm_floor_episodes"] = dist
fig, ax = plt.subplots(figsize=(9, 3.6))
cols = ["#9dc8f7", SERIES[0], SERIES[1], SERIES[2], SERIES[6], GRAY]
lefts = [0] * len(arms)
for c, col in zip(cats, cols):
    vals = [dist[a][c] for a in arms]
    ax.barh(arms, vals, left=lefts, color=col, label=c, edgecolor="white", linewidth=2)
    for i, v in enumerate(vals):
        if v >= 40: ax.text(lefts[i] + v / 2, i, str(v), ha="center", va="center", fontsize=8, fontweight="bold",
                            color="#0b0b0b" if col in ("#9dc8f7", GRAY) else "white")
    lefts = [l + v for l, v in zip(lefts, vals)]
for i, t in enumerate(lefts):
    ax.text(t + 8, i, f"{t:,}", va="center", fontsize=9)
ax.grid(axis="y", visible=False); ax.invert_yaxis(); ax.set_xlabel("에피소드"); ax.legend(ncol=6, loc="lower right", fontsize=8, bbox_to_anchor=(1, 1.0))
ax.set_title("팔·층별 텔레옵 에피소드 분포", loc="left", pad=24)
save(fig, "06_arm_floor_distribution", "docs/dataset-inventory.csv (kind=teleop)",
     "Left=B팔(왼팔), Right=A팔(오른팔), Front=앞팔, Both=양팔 동시 녹화. 기타=층 정보 없음")

# ---------- 7. wrist boundary fix (S01 table + per-folder) ----------
# Values from the wrist-fix verification (docs/wrist-fix-analysis.md, recomputed 11-22).
wf = {"metric": ["|a-s| 중앙값", "p95", "최대"], "before": [145.35, 146.47, 151.89], "after": [0.29, 2.39, 5.81],
      "jumps_before": 49, "jumps_after": 0}
DATA["wrist_fix_S01"] = wf
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [2.2, 1]})
x = range(3)
axes[0].bar([i - 0.2 for i in x], wf["before"], 0.38, color=BAD, label="보정 전 (원본)")
axes[0].bar([i + 0.2 for i in x], wf["after"], 0.38, color=SERIES[0], label="보정 후 (wristfix)")
for i in x:
    axes[0].text(i - 0.2, wf["before"][i] + 2, f'{wf["before"][i]:.1f}', ha="center", fontsize=8)
    axes[0].text(i + 0.2, wf["after"][i] + 2, f'{wf["after"][i]:.2f}', ha="center", fontsize=8)
axes[0].set_xticks(list(x), wf["metric"]); axes[0].set_ylabel("wrist_roll |action - state| (정규화 단위, ±100)")
axes[0].legend(loc="lower left", bbox_to_anchor=(0, 1.08), ncol=2); axes[0].set_title("손목 경계 보정 전후 — action·state 차이", loc="left", fontsize=11, pad=30)
axes[1].bar(["보정 전", "보정 후"], [wf["jumps_before"], wf["jumps_after"]], color=[BAD, SERIES[0]], width=0.55)
axes[1].text(0, 50.5, "49", ha="center"); axes[1].text(1, 1.5, "0", ha="center")
axes[1].set_ylabel("50 넘는 프레임 간 점프 (회)"); axes[1].set_title("±100 경계 점프", loc="left", fontsize=11, pad=30)
save(fig, "07_wrist_fix_before_after", "docs/wrist-fix-analysis.md (Left_11_21_F02_S01, _wristfix_records_20261122 검증값)",
     "B팔 F02 S01 10 ep; 보정 = fold(action + 폴더별 오프셋 53.97). 6개 폴더 전체: 중앙값 52~55→0.3~0.6, 점프 32~49→0")

# ---------- 8. camera alignment (top camera, F01 S03) ----------
cw = json.load(open(REP / "hf_real_eval_20261127" / "f01_s03" / "kit" / "top_cam_warp.json"))
cam = {"before": {"shift_px": (cw["shift_px"][0] ** 2 + cw["shift_px"][1] ** 2) ** 0.5, "rot_deg": abs(cw["rot_deg"])},
       "after": {"shift_px": (cw["residual_vs_11_23"]["shift_px"][0] ** 2 + cw["residual_vs_11_23"]["shift_px"][1] ** 2) ** 0.5,
                 "rot_deg": abs(cw["residual_vs_11_23"]["rot_deg"])},
       "inliers": f'{cw["inliers"]}/{cw["matches"]}'}
DATA["camera_alignment_top"] = cam
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
for ax, k, unit in zip(axes, ("shift_px", "rot_deg"), ("이동 오차 (px)", "회전 오차 (°)")):
    v = [cam["before"][k], cam["after"][k]]
    ax.bar(["보정 전\n(라이브 vs 학습)", "보정 후\n(잔차)"], v, color=[BAD, SERIES[0]], width=0.55)
    for i, t in enumerate(v):
        ax.text(i, t * 1.02 + (0.2 if k == "shift_px" else 0.01), f"{t:.2f}", ha="center")
    ax.set_ylabel(unit)
axes[0].set_title("탑뷰 카메라 정합 전후", loc="left")
save(fig, "08_camera_alignment", "f01_s03/kit/top_cam_warp.json (특징점 정합, 11-26)",
     f"B팔 F01 S03, 640×480, 기준=학습 데이터 L_11_23_F01_S03 ep0 frame0, inliers {cam['inliers']}. 효과(성공률 향상)는 미확정")

# ---------- 9. physical validation outcomes ----------
def classify_f01(r):
    p = r["place(놓기)"]
    if r["trial"] == "2": return "성공"
    if p.startswith("성공"): return "부분 성공"
    return "실패"
def classify_f02(r):
    if r["place(S05 2층 놓기)"].startswith("성공"):
        return "성공" if r["collision(다른 컨테이너 교란)"].startswith("없음") else "부분 성공"
    return "실패"
f01 = list(csv.DictReader(open(REP / "hf_real_eval_20261127" / "f01_s03" / "results.csv")))
f02 = [r for r in csv.DictReader(open(REP / "hf_real_eval_20261127" / "f02_s05" / "results.csv"))
       if "bottomwarp" not in r["model"]]
groups = collections.OrderedDict()
groups["B F01 S03\nACT"] = collections.Counter(classify_f01(r) for r in f01)
groups["B F02 S05\nACT"] = collections.Counter(classify_f02(r) for r in f02)
groups["B F02 S01\n리플레이"] = collections.Counter({"성공": 1})
groups["B F03 S02\n리플레이"] = collections.Counter({"부분 성공": 2})  # 배치 정밀도 미흡 (2026-11-28 재판정)
groups["B F01 S03\n리플레이 11-28"] = collections.Counter({"성공": 5, "부분 성공": 1})
DATA["physical_outcomes"] = {k.replace("\n", " "): dict(v) for k, v in groups.items()}
fig, ax = plt.subplots(figsize=(10, 4.2))
order = [("성공", GOOD), ("부분 성공", PART), ("실패", BAD)]
names = list(groups); left = [0] * len(names)
for lab_, col in order:
    vals = [groups[n].get(lab_, 0) for n in names]
    ax.barh(names, vals, left=left, color=col, label=lab_, edgecolor="white", linewidth=2)
    for i, v in enumerate(vals):
        if v: ax.text(left[i] + v / 2, i, str(v), ha="center", va="center", fontsize=9, fontweight="bold",
                      color="#0b0b0b" if col == PART else "white")
    left = [a + b for a, b in zip(left, vals)]
for i, t in enumerate(left):
    ax.text(t + 0.2, i, f"n={t}", va="center", fontsize=8.5, color=INK2)
ax.grid(axis="y", visible=False); ax.invert_yaxis(); ax.set_xlabel("실행 횟수"); ax.legend(ncol=3, loc="lower right", bbox_to_anchor=(1, 1.0))
ax.set_title("실물 검증 결과 — ACT 자율 구동 vs 녹화 리플레이", loc="left", pad=22)
save(fig, "09_physical_outcomes",
     "hf_real_eval_20261127/f01_s03·f02_s05/results.csv, lf02/lf03 replay RESULT, final_20261128/REPRESENTATIVE_VIDEOS.md",
     "성공=놓기 성공+교란 없음, 부분=놓기는 했으나 충돌·끌기·사람 개입·배치 정밀도 미흡, 실패=놓기 실패. F02 S05는 보정 없는 설정 7회(bottomwarp 2회 제외). "
     "F01 S03 리플레이 11-28: 영상 손상 1회는 판정 불가로 제외")

# ---------- 10. offline sim vs physical ----------
s03 = json.load(open(LOGS / "b-f01-act-run-20261126" / "s03_s05_reach.json"))
f2r = json.load(open(LOGS / "b-f02-ex-prep-20261126" / "f02_spot_reach.json"))
sim_s03 = [v["ok"] for k, v in s03.items() if "_S03_" in k]
sim_s05 = [v["ok"] for k, v in f2r.items() if k.startswith("S05_")]
phys = {"F01 S03": (groups["B F01 S03\nACT"]["성공"], sum(groups["B F01 S03\nACT"].values())),
        "F02 S05": (groups["B F02 S05\nACT"]["성공"], sum(groups["B F02 S05\nACT"].values()))}
cmp_ = {"F01 S03": {"offline": (sum(sim_s03), len(sim_s03)), "physical": phys["F01 S03"]},
        "F02 S05": {"offline": (sum(sim_s05), len(sim_s05)), "physical": phys["F02 S05"]}}
DATA["offline_vs_physical"] = cmp_
fig, ax = plt.subplots(figsize=(8, 3.8))
for i, (k, v) in enumerate(cmp_.items()):
    for j, (kind, col) in enumerate((("offline", GRAY), ("physical", SERIES[0]))):
        a, n = v[kind]; r = 100 * a / n
        ax.bar(i + (j - 0.5) * 0.4, r, 0.38, color=col, label=("오프라인 폐루프 근사 시뮬" if kind == "offline" else "실물 ACT (깨끗한 성공)") if i == 0 else None)
        ax.text(i + (j - 0.5) * 0.4, r + 2, f"{a}/{n}\n({r:.0f}%)", ha="center", fontsize=8.5)
ax.set_xticks([0, 1], ["B팔 F01 S03\n(Best 12000)", "B팔 F02 S05\n(wristfix Best 12000)"])
ax.set_ylabel("성공률 (%)"); ax.set_ylim(0, 115); ax.legend(loc="upper left", ncol=2)
ax.set_title("오프라인 평가 vs 실물 평가", loc="left")
save(fig, "10_offline_vs_physical",
     "b-f01-act-run-20261126/s03_s05_reach.json, b-f02-ex-prep-20261126/f02_spot_reach.json, results.csv",
     "오프라인 = 녹화 영상 입력 폐루프 근사(집기·놓기 자세 오차 기준), 실물 = 실제 로봇 ACT 실행. 표본이 작아(7~15회) 비율은 참고용")

json.dump({"sources": SOURCES, "data": DATA}, open(OUT / "graph_data.json", "w"), ensure_ascii=False, indent=1)
print("\n".join(sorted(SOURCES)))
