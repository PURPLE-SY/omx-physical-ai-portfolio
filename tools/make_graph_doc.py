"""Write docs/graphs.md (graph list + data tables) from assets/graphs/graph_data.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
g = json.load(open(ROOT / "assets/graphs/graph_data.json"))
S, D = g["sources"], g["data"]
L = ["# 학습·검증 그래프", "", "작성: **PURPLE-SY (김승용)**", "",
     "모든 그래프는 기록된 로그에서 다시 그렸습니다. 로그가 없는 항목은 그리지 않고 아래 **없는 그래프**에 적었습니다.",
     "다시 만들기: `python tools/make_graphs.py <src_light> <src_backup>` (외장 HDD 백업 사본 경로). 그린 숫자는 [`graph_data.json`](../assets/graphs/graph_data.json)에 그대로 있습니다.",
     "각 그래프 아래 표는 색을 구분하기 어려울 때 읽는 데이터 표입니다.", ""]
TITLES = {
    "01_training_loss": "1. ACT Training Loss", "02_validation_loss": "2. Validation Loss",
    "03_best_vs_final": "3. Best vs Final 모델", "04_joint_prediction_error": "4. 관절별 예측값 vs 실제값 오차",
    "05_daily_collection": "5. 날짜별 수집량과 누적 에피소드", "06_arm_floor_distribution": "6. 팔·층별 데이터 분포",
    "07_wrist_fix_before_after": "7. 손목 경계 보정 전후", "08_camera_alignment": "8. 카메라 정합 전후 오차",
    "09_physical_outcomes": "9. 실물 검증 결과(성공·부분 성공·실패)", "10_offline_vs_physical": "10. 오프라인 평가 vs 실물 평가",
}
for name, title in TITLES.items():
    L += [f"## {title}", "", f"![{title}](../assets/graphs/{name}.png)", "",
          f"- **조건:** {S[name]['condition']}", f"- **출처:** `{S[name]['source']}`", ""]
    if name in ("01_training_loss", "02_validation_loss"):
        k = 1 if name.startswith("01") else 2
        models = list(D["checkpoint_losses"])
        steps = [r[0] for r in D["checkpoint_losses"][models[0]]]
        L += ["| step | " + " | ".join(models) + " |", "|---:|" + "---:|" * len(models)]
        for i, s in enumerate(steps):
            L.append(f"| {s:,} | " + " | ".join(f"{D['checkpoint_losses'][m][i][k]:.4g}" for m in models) + " |")
    elif name == "03_best_vs_final":
        L += ["| 모델 | Best step | Best val | Final step | Final val |", "|---|---:|---:|---:|---:|"]
        for m, v in D["best_vs_final"].items():
            L.append(f"| {m} | {v['best_step']:,} | {v['best']:.4f} | {v['final_step']:,} | {v['final']:.4f} |")
    elif name == "04_joint_prediction_error":
        j = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper"]
        L += ["| 체크포인트 | 지표 | " + " | ".join(j) + " |", "|---|---|" + "---:|" * 6]
        for ck, v in D["joint_mae_b_f02"].items():
            for met in ("first_mae", "chunk_mae"):
                L.append(f"| {int(ck):,} | {met} | " + " | ".join(f"{x:.2f}" for x in v[met]) + " |")
    elif name == "05_daily_collection":
        L += ["| 날짜 | 에피소드 | 누적 |", "|---|---:|---:|"]
        for d, v in D["daily_episodes"]["daily"].items():
            L.append(f"| {d} | {v} | {D['daily_episodes']['cumulative'][d]:,} |")
    elif name == "06_arm_floor_distribution":
        cats = list(next(iter(D["arm_floor_episodes"].values())))
        L += ["| 팔 | " + " | ".join(cats) + " | 합계 |", "|---|" + "---:|" * (len(cats) + 1)]
        for a, v in D["arm_floor_episodes"].items():
            L.append(f"| {a} | " + " | ".join(str(v[c]) for c in cats) + f" | {sum(v.values())} |")
    elif name == "07_wrist_fix_before_after":
        w = D["wrist_fix_S01"]
        L += ["| 지표 | 보정 전 | 보정 후 |", "|---|---:|---:|"]
        for m, b, a in zip(w["metric"], w["before"], w["after"]):
            L.append(f"| {m} | {b} | {a} |")
        L.append(f"| 50 넘는 프레임 간 점프 | {w['jumps_before']} | {w['jumps_after']} |")
        L += ["", "원래 시계열(실제 녹화 1개 에피소드의 state와 action):", "",
              "![손목 보정 전후 시계열](../assets/graphs/11_replay_fig4_wrist_before_after.png)"]
    elif name == "08_camera_alignment":
        c = D["camera_alignment_top"]
        L += ["| | 이동 (px) | 회전 (°) |", "|---|---:|---:|",
              f"| 보정 전 | {c['before']['shift_px']:.2f} | {c['before']['rot_deg']:.3f} |",
              f"| 보정 후 잔차 | {c['after']['shift_px']:.2f} | {c['after']['rot_deg']:.3f} |", "",
              "- 반투명(50 %) 비교 이미지: [증빙 이미지](evidence-gallery.md#카메라-정합)",
              "- 주의: F02 S05에서는 카메라가 학습 구도로 돌아와 있어 같은 보정을 적용하면 오히려 (-37, -9) px 어긋났습니다. 그래서 그 실행은 보정 없이 했습니다. 보정 효과(성공률 향상)는 확정하지 못했습니다."]
    elif name == "09_physical_outcomes":
        L += ["| 실행 | 성공 | 부분 성공 | 실패 | 합계 |", "|---|---:|---:|---:|---:|"]
        for k, v in D["physical_outcomes"].items():
            L.append(f"| {k} | {v.get('성공', 0)} | {v.get('부분 성공', 0)} | {v.get('실패', 0)} | {sum(v.values())} |")
    elif name == "10_offline_vs_physical":
        L += ["| 위치 | 오프라인 성공 | 실물 깨끗한 성공 |", "|---|---:|---:|"]
        for k, v in D["offline_vs_physical"].items():
            L.append(f"| {k} | {v['offline'][0]}/{v['offline'][1]} | {v['physical'][0]}/{v['physical'][1]} |")
        L += ["", "오프라인 근사가 실물보다 높게 나옵니다. 근사는 실제 접촉, 다른 컨테이너와의 충돌, 카메라 이동을 반영하지 않습니다."]
    L.append("")

L += ["## 11. 모터 부하·관절 추종 오차 (리플레이 실측)", "",
      "F02 S01 리플레이(2026-11-25, 0.25배속) 실행 중 0.1초마다 기록한 값입니다. 노트북에서 만든 원본 그림을 그대로 씁니다(데이터: [`11_replay_figures_data.json`](../assets/graphs/11_replay_figures_data.json)).", "",
      "![추종 오차 최대·평균](../assets/graphs/11_replay_fig1_tracking_error_max_mean.png)",
      "![추종 오차 시계열](../assets/graphs/11_replay_fig2_tracking_error_timeseries.png)",
      "![전압·온도·부하](../assets/graphs/11_replay_fig3_voltage_temperature_load.png)",
      "![녹화 vs 리플레이](../assets/graphs/11_replay_fig5_recorded_vs_replay.png)", "",
      "- gripper 추종 오차가 큰 구간은 블록을 쥐고 있어 명령만큼 닫히지 못하는 시간입니다(정상).",
      "- ACT 실행 중 부하는 그래프 없이 로그 최대값만 있습니다: F01 S03 23:48 성공 때 lift 281 / elbow 230, step limit 5 시험 때 358 / 331. F02 S05 elbow 최대 403~463 (bottomwarp 실패 때 511).", "",
      "## 12. 학습 모니터 원본 그림", "",
      "학습 PC 모니터가 저장한 B팔 F02 wristfix 학습 그래프 원본입니다.", "",
      "![학습 모니터 loss](../assets/graphs/12_lf02_training_monitor_loss.png)", "",
      "## 없는 그래프 (로그 없음 — 만들지 않음)", "",
      "| 요청 항목 | 상태 |",
      "|---|---|",
      "| 학습 모니터 **화면 스크린샷** | 모니터 HTML(`OMX ACT 학습 모니터.html`)만 남아 있고 화면 캡처 파일은 없음. 대신 모니터가 저장한 loss 그림(12번)을 씀 |",
      "| ACT 실행 중 관절별 추종 오차 시계열 | 실행 로그에는 최대 부하만 있음. 리플레이(11번)만 시계열 있음 |",
      "| A팔(오른팔) 실물 결과 | A팔은 읽기 전용 점검만 했고 실물 구동 기록 없음 |",
      "| 11-28 00:41~01:38 앱 실행 결과 | 판정 기록 없음(영상 36개 미판정) |",
      ]
import re
out = re.sub(r"(?<=[^\s`])~(?=[^\s/])", "–", "\n".join(L) + "\n")  # GFM would strike through a~b
(ROOT / "docs/graphs.md").write_text(out, encoding="utf-8")
print("ok")
