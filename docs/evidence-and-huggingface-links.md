# 증빙과 Hugging Face 링크

## 접근 권한 안내
- 이 포트폴리오는 공개 저장소다. 원본 영상과 모델 가중치는 GitHub에 올리지 않았다.
- **공개 HF 저장소:** 링크로 바로 열 수 있다(2026-11-07~11-24 원본 대부분, 10/29~11/04 왼팔·앞팔 원본, 11-10 평가 기록).
- **비공개 HF 저장소:** 링크 없이 이름과 "HF 비공개"로만 표시했다. 신규 원본 10개, 손목 보정 합본, 학습 모델, 실물 검증 증빙이 여기에 해당한다. 원본 녹화와 민감한 실험 자료는 비공개로 유지하는 것이 운영 방침이다.

## 원본 데이터셋
- 전체 목록과 링크: [dataset-inventory.csv](dataset-inventory.csv) (`hf_url` 열)
- 날짜별 표: [data-collection-timeline.md](data-collection-timeline.md)

**SHA-256 검증 (2026-11-27):**

| 대상 | 폴더 | ep | frames | 파일 | 용량 | 결과 |
|---|---|---|---|---|---|---|
| 기존 원본 (로컬 ↔ HF) | 78쌍 | 1,067 | 657,856 | 979 | 27.7 GB | 전부 일치 |
| 신규 비공개 업로드 | 10개 | 40 | 75,404 | 102 | 2.83 GB | 102/102 일치 |

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
