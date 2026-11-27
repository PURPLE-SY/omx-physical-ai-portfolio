# 증빙과 Hugging Face 저장소

## 접근 권한 안내
- 이 포트폴리오는 공개 저장소다. 원본 영상과 모델 가중치는 GitHub에 올리지 않았다.
- **HF 직접 링크는 게시하지 않았다.** OMX 원본 녹화는 팀 프로젝트 자료이고, 저장소별 팀 공개 권한이 아직 확인되지 않았기 때문이다. 현재 HF에서 공개 상태인 저장소도 마찬가지다.
  - 문서에는 저장소 이름, 현재 공개 상태(`dataset-inventory.csv`의 `hf_visibility_now`), 통계, 검증 결과만 적었다.
  - 저장소별 공개 권한이 확인되면 승인된 링크만 다시 추가한다.
- 비공개로 유지하는 자료: 신규 원본 10개, 손목 보정 합본, 학습 모델, 실물 검증 증빙(영상·로그·eval)

## HF 저장소 수 (2026-11-27, 고유 repository ID 기준)
| 구분 | 수 |
|---|---|
| HF 전체 | 111 (데이터셋 88, 모델 23) |
| HF 현재 공개 | 74 (데이터셋 73, 모델 1) |
| `dataset-inventory.csv` 행 | 95 (고유 저장소 84) |
| CSV에서 현재 공개 행 | 83 (고유 저장소 72) |

- **83행이 72개로 줄어드는 이유:** `Purple-SY/omx-left-arm` 한 저장소에 날짜별 하위 데이터셋 12개(2026-10-29_v8 ~ 2026-11-03_v25)가 들어 있어 12행으로 집계됨
- **74개와 72개의 차이 2개:** 녹화 데이터셋이 아니라서 CSV에 넣지 않은 저장소
  - 실험 보고서 데이터셋 `Purple-SY/act-evaluation-failure-20261110`
  - 모델 `Purple-SY/omx-act-pick-place-1110-10k`

## 원본 데이터셋
- 전체 목록: [dataset-inventory.csv](dataset-inventory.csv) (`hf_repo`, `hf_visibility_now` 열)
- 날짜별 표: [data-collection-timeline.md](data-collection-timeline.md)

**SHA-256 검증 (2026-11-27):**

| 대상 | 폴더 | ep | frames | 파일 | 용량 | 결과 |
|---|---|---|---|---|---|---|
| 기존 원본 (로컬 ↔ HF) | 78쌍 | 1,067 | 657,856 | 979 | 27.7 GB | 전부 일치 |
| 신규 비공개 업로드 | 10개 | 40 | 75,404 | 102 | 2.83 GB | 102/102 일치 |

**두 숫자가 녹화량 합계(1,085 ep / 706,919 frames)와 다른 이유:**

| 구분 | 폴더 | ep | frames |
|---|---|---|---|
| 78쌍 중 텔레옵 원본 | 69 | 976 | 576,770 |
| 78쌍 중 ACT 평가 기록(11-10) | 6 | 6 | 2,406 |
| 78쌍 중 합본(LF02 wristfix merged 60, R_11_22_EX_seam16 16, 11_10_all 9) | 3 | 85 | 78,680 |
| HF에만 있는 텔레옵 원본(omx-left-arm 10/29~10/31 6개, 11_10_spot02) | 7 | 70 | 55,352 |
| 신규 10개 중 텔레옵 원본(TEST 2 ep, 양팔 관절값 전용 1 ep 포함) | 9 | 39 | 74,797 |
| 신규 10개 중 진단 녹화(diag_S06_20261114) | 1 | 1 | 607 |
| **녹화량 합계 = 976 + 70 + 39** | **85** | **1,085** | **706,919** |

- HF에만 있는 원본(omx-left-arm 10/29~10/31 하위 폴더 6개, pick_place_11_10_spot02)은 로컬 원본이 없어 대조 불가

## 실물 검증 증빙 (HF 비공개)
- F01 S03: `Purple-SY/omx-b-arm-f01-s03-real-eval-20261126` (HF 비공개)
- F02 S01 리플레이: `Purple-SY/omx-b-arm-f02-s01-real-replay-20261125` (HF 비공개)
- F02 S05: `Purple-SY/omx-b-arm-f02-s05-real-eval-20261127` (HF 비공개)

## 모델 (HF 비공개)
- `Purple-SY/omx-act-arm-a-f01-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-a-f02-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-a-f03-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-a-ex-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-b-f01-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-b-f02-wristfix-13k-1124` (HF 비공개)
- `Purple-SY/omx-act-arm-b-ex-13k-1124` (HF 비공개)
- `Purple-SY/omx-left-arm-act-demo-20261126` (HF 비공개)

## 이 저장소에 넣지 않은 것
- 원본 영상, 모델 가중치, eval 녹화(HF에 있음)
- 팀 저장소 코드
- 장치 시리얼, 토큰, 이메일, 네트워크 정보
