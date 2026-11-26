# OMX Physical AI 엔지니어링 포트폴리오 (2026-10 ~ 2026-11)

**프로젝트:** OpenMANIPULATOR-X(OMX) 로봇 팔로 컨테이너를 집어 트레이(층·자리별)에 놓는 작업을 ACT 모방학습으로 구현하는 팀 프로젝트. 이 저장소는 그중 **내가 직접 수행한** 데이터 수집·품질 분석·학습 결과 관리·실물 검증을 정리한 것이다.

모든 수치는 원본 파일(LeRobot `meta/info.json`, 실행 로그, 탑뷰 영상, HF 저장소)에서 다시 집계했다. 확인하지 못한 값은 **미확인**으로 표시했다.

## 핵심 성과
- **녹화:** 텔레옵 원본 **85개 폴더 / 1,085 에피소드 / 706,919 프레임** (2026-10-29 ~ 11-25, 로컬·HF 중복 제외)
- **데이터 보존:** Hugging Face Purple-SY에 원본 정리
  - 기존 78쌍 SHA-256 전부 일치
  - 누락 원본 10개 비공개 추가 업로드, 102/102 일치
- **데이터 오류 해결:**
  - 11/14 시간축 압축(표기 30 Hz ↔ 실제 13~15 Hz) 분석
  - Left F02 손목 action 오프셋(51.4~55.3) 보정 → \|a−s\| 중앙값 145 → 0.3
- **ACT 학습:** 13,000-step 모델 7종(189파일, 8.05 GB) 학습 결과 관리, Best val loss 0.21~0.33 — 실물 성공률과 별개
- **실물 검증 (성공·실패 모두 기록):**

| 검증 | 내용 | 결과 |
|---|---|---|
| [B팔 F01 S03](docs/physical-validation-F01-S03.md) | ACT 정책 실물 15회 | 집기 10, 놓기 4, 트레이 교란 없는 완전 성공 1 |
| [B팔 F02 S01](docs/physical-validation-F02-S01.md) | **녹화 데이터 리플레이**(정책 추론 아님) ep7 635 frames, 0.25배속 85.5 s | 1회 성공 |
| [B팔 F02 S05](docs/physical-validation-F02-S05.md) | ACT 정책, 보정 없는 설정 7회 (+ 보정 시도 2회 별도) | 깨끗한 성공 4, 2층 충돌 3 |

## 날짜별 수집량 (텔레옵 원본)
| 녹화일 | 폴더 | Episodes | Frames | 누적 Episodes | 팔 |
|---|---|---|---|---|---|
| 2026-10-29 | 1 | 10 | 11,453 | 10 | Left |
| 2026-10-30 | 3 | 30 | 26,281 | 40 | Left |
| 2026-10-31 | 4 | 31 | 30,602 | 71 | Left |
| 2026-11-02 | 2 | 50 | 27,326 | 121 | Left |
| 2026-11-03 | 4 | 35 | 22,759 | 156 | Front, Left |
| 2026-11-04 | 1 | 23 | 9,305 | 179 | Left |
| 2026-11-07 | 7 | 175 | 84,691 | 354 | Left |
| 2026-11-09 | 1 | 33 | 10,253 | 387 | Left |
| 2026-11-10 | 3 | 38 | 16,638 | 425 | Left |
| 2026-11-11 | 3 | 74 | 35,060 | 499 | Left |
| 2026-11-14 | 6 | 158 | 72,660 | 657 | Left |
| 2026-11-17 | 2 | 61 | 31,047 | 718 | Right |
| 2026-11-18 | 1 | 30 | 16,539 | 748 | Right |
| 2026-11-19 | 1 | 1 | 1,504 | 749 | Both |
| 2026-11-21 | 24 | 180 | 150,298 | 929 | Left, Right |
| 2026-11-22 | 7 | 37 | 72,333 | 966 | Left, Right |
| 2026-11-23 | 9 | 90 | 67,211 | 1056 | Left |
| 2026-11-24 | 5 | 28 | 19,999 | 1084 | Left, Right |
| 2026-11-25 | 1 | 1 | 960 | 1085 | Right |
| **합계** | **85** | **1085** | **706,919** | | |

- 세부 내역(팔·층·위치·폴더·카메라·HF 링크): [docs/data-collection-timeline.md](docs/data-collection-timeline.md), [docs/dataset-inventory.csv](docs/dataset-inventory.csv)
- 10/17~10/28 녹화 원본은 찾지 못함(미확인). 11/26~27은 실물 검증만 있고 신규 녹화는 없음.

## 대표 오류 분석
1. **시간축 압축 (11/14, 158 ep):** 행마다 timestamp를 1/30 s로 고정해, 실제 38.26 s가 16.0 s로 저장됨. 관절·행동 시간축도 함께 압축됨
2. **손목 오프셋 (Left F02, 60 ep):** 녹화 코드 수정 전 버전으로 녹화됨
   - 보정 데이터로 13k 재학습
   - 기존 모델은 dry-run 게이트 FAIL 7개로 실물 실행 금지
3. **복귀 중 충돌 (실물):** shoulder_lift 추종 지연이 학습 대비 2~2.5배 — **원인 후보, 미확정**

## 문서
| 문서 | 내용 |
|---|---|
| [data-collection-timeline.md](docs/data-collection-timeline.md) | 날짜·팔·층·위치별 녹화 이력, 기존 수치 대조 |
| [dataset-inventory.csv](docs/dataset-inventory.csv) | 데이터셋 전체 목록(95행: 원본 85 + 합본·평가·진단 10) |
| [data-quality-analysis.md](docs/data-quality-analysis.md) | 시간축, 0.5 s 정지, dry-run 실패, 재검증, 파생 데이터 |
| [wrist-fix-analysis.md](docs/wrist-fix-analysis.md) | 손목 오프셋 원본 vs 보정본 |
| [act-training-history.md](docs/act-training-history.md) | 모델·데이터·loss·HF 링크 |
| [physical-validation-F01-S03.md](docs/physical-validation-F01-S03.md) · [F02-S01](docs/physical-validation-F02-S01.md) · [F02-S05](docs/physical-validation-F02-S05.md) | 실물 검증 3건 |
| [hardware-debugging.md](docs/hardware-debugging.md) | 모터·통신·카메라 문제 이력 |
| [engineering-contribution.md](docs/engineering-contribution.md) | 내가 수행한 역할 |
| [interview-summary.md](docs/interview-summary.md) | 면접용 요약 |
| [evidence-and-huggingface-links.md](docs/evidence-and-huggingface-links.md) | HF 링크, SHA-256 결과, 접근 권한 |
| [scripts/](scripts/README.md) | 실행 흔적이 확인된 분석·점검 스크립트(출처 명시) |

## 공개 범위와 증빙 접근
- 이 저장소는 **공개 저장소**다. 공개 전에 팀 내부 정보, 다른 팀원의 코드, 인증정보, 개인정보, 장치 식별자를 검사했다.
- **링크로 바로 열 수 있는 증빙:** 공개 HF 데이터셋(`docs/dataset-inventory.csv`에서 `hf_access=public`인 83개 행)
- **비공개로 유지하는 자료:** 신규 원본 녹화, 학습 모델, 실물 검증 증빙(영상·로그·eval)
  - 공개 정책에 따라 HF 비공개 저장소에 두고, 문서에는 이름과 "HF 비공개"만 표시했다
- 이 문서의 통계는 위 원본에서 다시 집계한 값이다. 집계와 검증에 쓴 스크립트는 `scripts/`에 있다.
