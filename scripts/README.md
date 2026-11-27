# 스크립트 (실행 흔적이 확인된 것만 포함)

**출처와 작성 방식(사실대로):**
- 아래 파일은 개인 작업 폴더(`~/omx_logs`, `~/omx_datasets/_wristfix_records_20261122`)에 있던 분석·점검 도구의 복사본이다. 팀 저장소 코드는 넣지 않았다.
- 모두 내가 AI 코딩 도구(Claude Code, Codex)에 지시하고 결과를 검토하며 만든 것이다. 단독으로 손으로 작성한 코드라고 주장하지 않는다.
- 복사하면서 USB·RealSense 장치 시리얼만 `<USB_SERIAL>`, `<REALSENSE_SERIAL>`로 바꿨다. 그 외에는 원본 그대로다.
- 경로가 작업 PC 기준(`/home/purple/...`)이라 다른 환경에서 바로 실행되지는 않는다.

| 파일 | 용도 | 모터 사용 | 실행 근거 (작업 PC) |
|---|---|---|---|
| evaluation/offline_dryrun.py, offline_dryrun_lib.py | 녹화 영상 → 정책 → 실행 명령 체인 오프라인 재현 | 없음 | `b-f01-act-run-20261126/offline_dryrun.json` |
| evaluation/closedloop_sim.py | 폐루프 근사 시뮬레이션(관절 제한·스텝 제한 포함) | 없음 | `closedloop_sim.json` |
| evaluation/f02_spot_reach.py | F02 자리별 폐루프 근사 집기·놓기 오차 비교 | 없음 | `b-f02-ex-prep-20261126/f02_spot_reach.json` |
| data_quality/wristfix_apply.py | Left F02 손목 action 오프셋 보정(새 폴더에만 씀) | 없음 | `wristfix_manifest.json` |
| data_quality/wristfix_verify.py, merge_verify.py | 보정 전후 지표, 병합본 프레임 단위 일치 검증 | 없음 | `wristfix_verify.json`, `merge_verify.json` |
| inventory/hf_13k_audit_report.py | 13k 모델 HF 업로드 감사 보고서 생성 | 없음 | `hf-13k-1124-audit/REPORT.md` |
| inventory/scan_local_datasets.py | 로컬 LeRobot 데이터셋 에피소드·프레임 집계 | 없음 | 2026-11-27 이 포트폴리오 작업 중 작성·실행 |
| inventory/verify_hf_sha256.py | 로컬 원본과 HF 파일 SHA-256 대조 | 없음 | 2026-11-27 실행(78쌍 일치) |

실물 실행 전 안전 점검 도구(`preflight`)는 팀 저장소 모듈과 팀 저장소 경로를 참조해서 공개본에서 뺐다. 내용은 `docs/physical-validation-F02-S05.md`에 설명으로만 남겼다.

요청 목록 중 **"Auto Homing 오프라인 검증 초안"**은 팀 저장소의 미병합 브랜치에 본인 커밋 2건(2026-11-25)으로 있다. 모터를 쓰지 않는 오프라인 homing 계획·검증과 B팔 F02 Best12000 CPU 점검을 다룬다. 팀 저장소 코드라 공개본에는 포함하지 않았다.
