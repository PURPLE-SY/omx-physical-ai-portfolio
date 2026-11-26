# 날짜별 녹화 이력 (2026-10-17 ~ 2026-11-27)

근거: `dataset-inventory.csv` (로컬 `~/omx_datasets` 원본 + HF Purple-SY 저장소, 각 데이터셋 `meta/info.json`의 `total_episodes`·`total_frames`).
- **녹화일**: HF README 분류표 또는 폴더 이름의 날짜. **저장일**: 로컬 첫 data parquet 파일 수정 시각(`saved_local` 열). HF에만 있는 자료는 저장일 미확인.
- 같은 원본이 로컬과 HF에 함께 있으면 1건으로만 셈. 합본·가공본(`no_wrist`, `11_07_OR_all`, `11_10_all`, `LF02 wristfix merged`, `R_11_22_EX_seam16`, HDD 학습 합본), ACT 평가 실행 기록, 진단 녹화는 녹화량 합계에서 제외(별도 표).
- 10/17~10/28 녹화 원본은 로컬·외장 HDD·HF 어디에서도 찾지 못함(미확인). 11/26~11/27 신규 텔레옵 녹화 원본도 없음(11/26~27은 실물 검증 실행만 있음).

## 1. 날짜별 합계 (텔레옵 원본만)

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

## 2. 기존에 알려진 수치와 대조

| 알려진 기록 | 재계산 | 판정 |
|---|---|---|
| 10/31 20ep | v19 10 + v20 10 = 20 (로컬). HF에는 같은 날 v12_1ep 1 + v13 10도 있어 10/31 전체는 31ep | 20은 v19·v20만 센 값. 날짜 전체는 31 |
| 11/02 50ep | v22 30 + v23 20 = 50 | 일치 |
| 11/03 35ep | 앞팔 v1 20 + v2 10 + 왼팔 v24 3 + v25 2 = 35 | 일치 |
| 11/04 23ep | pick_place_11_04LEFT 23 | 일치 |
| 11/07 175ep | spot01~06_OR 155 + spot01_YE 20 = 175 | 일치 |
| 11/20 누적 688ep | 11/19까지 누적 749ep (10/29~10/30 HF 전용분 포함) | **미확인** — 688의 집계 기준을 찾지 못함 |
| 11/21 24폴더 180ep 150,298 frames | 24폴더 180ep 150,298 frames | 일치 |
| 11/23 Left F01 70ep 44,915 frames | F01 EX 10ep(14,225) + S01~S06 60ep(28,569) = 70ep **42,794 frames**. 11/23 전체는 F02_EX·F03_EX 포함 90ep 67,211 | ep 일치, **프레임 44,915 미확인** |

## 3. 날짜·팔·층·위치별 세부

| 녹화일 | 팔 | 층 | 위치 | 폴더 | Episodes | Frames | 카메라 | HF |
|---|---|---|---|---|---|---|---|---|
| 2026-10-29 | Left | 1층(층 구분 이전) | - | `2026-10-29_v8` | 10 | 11,453 | top|wrist | [omx-left-arm/2026-10-29_v8](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-29_v8) |
| 2026-10-30 | Left | 1층(층 구분 이전) | - | `2026-10-30_v10` | 10 | 7,800 | top|wrist | [omx-left-arm/2026-10-30_v10](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-30_v10) |
| 2026-10-30 | Left | 1층(층 구분 이전) | - | `2026-10-30_v11` | 10 | 10,277 | top|wrist | [omx-left-arm/2026-10-30_v11](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-30_v11) |
| 2026-10-30 | Left | 1층(층 구분 이전) | - | `2026-10-30_v9` | 10 | 8,204 | top|wrist | [omx-left-arm/2026-10-30_v9](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-30_v9) |
| 2026-10-31 | Left | 1층(층 구분 이전) | - | `2026-10-31_v12_1ep` | 1 | 626 | top|wrist | [omx-left-arm/2026-10-31_v12_1ep](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-31_v12_1ep) |
| 2026-10-31 | Left | 1층(층 구분 이전) | - | `2026-10-31_v13` | 10 | 8,673 | top|wrist | [omx-left-arm/2026-10-31_v13](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-31_v13) |
| 2026-10-31 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/10월 31일 모방 학습!` | 10 | 11,665 | top|wrist|SIDE | [omx-left-arm/2026-10-31_v19](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-31_v19) |
| 2026-10-31 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/pick_place_v20` | 10 | 9,638 | top|wrist|SIDE | [omx-left-arm/2026-10-31_v20](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-10-31_v20) |
| 2026-11-02 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/pick_place_v22` | 30 | 15,356 | top|wrist|SIDE | [omx-left-arm/2026-11-02_v22](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-11-02_v22) |
| 2026-11-02 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/pick_place_v23` | 20 | 11,970 | top|wrist|SIDE | [omx-left-arm/2026-11-02_v23](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-11-02_v23) |
| 2026-11-03 | Front | - | - | `front/pick_place_v1` | 20 | 14,246 | top|wrist | [omx-front-arm](https://huggingface.co/datasets/Purple-SY/omx-front-arm) |
| 2026-11-03 | Front | - | - | `front/pick_place_v2` | 10 | 6,976 | top|wrist | [omx-front-arm-v2](https://huggingface.co/datasets/Purple-SY/omx-front-arm-v2) |
| 2026-11-03 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/pick_place_v24` | 3 | 910 | top|wrist|SIDE | [omx-left-arm/2026-11-03_v24](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-11-03_v24) |
| 2026-11-03 | Left | 1층(층 구분 이전) | - | `left/wrist_degrees/pick_place_v25` | 2 | 627 | top|wrist|SIDE | [omx-left-arm/2026-11-03_v25](https://huggingface.co/datasets/Purple-SY/omx-left-arm/2026-11-03_v25) |
| 2026-11-04 | Left | 1층(층 구분 이전) | - | `pick_place_11_04LEFT` | 23 | 9,305 | top|wrist|rs|rs_depth | [omx-left-arm-20261104](https://huggingface.co/datasets/Purple-SY/omx-left-arm-20261104) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 1 | `pick_place_11_07_spot01_OR` | 21 | 10,163 | top|wrist|rs|rs_depth | [pick_place_11_07_spot01_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot01_OR) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 1 | `pick_place_11_07_spot01_YE` | 20 | 10,443 | top|wrist|rs|rs_depth | [pick_place_11_07_spot01_YE](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot01_YE) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 2 | `pick_place_11_07_spot02_OR` | 20 | 11,213 | top|wrist|rs|rs_depth | [pick_place_11_07_spot02_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot02_OR) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 3 | `pick_place_11_07_spot03_OR` | 21 | 9,382 | top|wrist|rs|rs_depth | [pick_place_11_07_spot03_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot03_OR) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 4 | `pick_place_11_07_spot04_OR` | 30 | 14,162 | top|wrist|rs|rs_depth | [pick_place_11_07_spot04_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot04_OR) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 5 | `pick_place_11_07_spot05_OR` | 30 | 14,775 | top|wrist|rs|rs_depth | [pick_place_11_07_spot05_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot05_OR) |
| 2026-11-07 | Left | 1층(층 구분 이전) | 스팟 6 | `pick_place_11_07_spot06_OR` | 33 | 14,553 | top|wrist|rs|rs_depth | [pick_place_11_07_spot06_OR](https://huggingface.co/datasets/Purple-SY/pick_place_11_07_spot06_OR) |
| 2026-11-09 | Left | 1층(층 구분 이전) | 스팟 1 | `pick_place_11_09_01spot` | 33 | 10,253 | top|wrist|rs|rs_depth | [pick_place_11_09_01spot](https://huggingface.co/datasets/Purple-SY/pick_place_11_09_01spot) |
| 2026-11-10 | Left | 1층(층 구분 이전) | - | `pick_place_11_10_02` | 13 | 5,664 | top|wrist|rs|rs_depth | [pick_place_11_10_02](https://huggingface.co/datasets/Purple-SY/pick_place_11_10_02) |
| 2026-11-10 | Left | 1층(층 구분 이전) | spot02 | `pick_place_11_10_spot02` | 19 | 8,319 | top|wrist|rs|rs_depth | [pick_place_11_10_spot02](https://huggingface.co/datasets/Purple-SY/pick_place_11_10_spot02) |
| 2026-11-10 | Left | 1층(층 구분 이전) | 스팟 2 | `pick_place_11_09_02spot` | 6 | 2,655 | top|wrist|rs|rs_depth | [pick_place_11_09_02spot](https://huggingface.co/datasets/Purple-SY/pick_place_11_09_02spot) |
| 2026-11-11 | Left | 1층(층 구분 이전) | 스팟 2 | `pick_place_11_10_spot_02` | 31 | 13,439 | top|wrist|rs|rs_depth | [pick_place_11_10_spot_02](https://huggingface.co/datasets/Purple-SY/pick_place_11_10_spot_02) |
| 2026-11-11 | Left | 1층(층 구분 이전) | 스팟 3 | `pick_place_11_11_spot_03` | 23 | 11,281 | top|wrist|rs|rs_depth | [pick_place_11_11_spot_03](https://huggingface.co/datasets/Purple-SY/pick_place_11_11_spot_03) |
| 2026-11-11 | Left | 1층(층 구분 이전) | 스팟 4 | `pick_place_11_11_spot_04` | 20 | 10,340 | top|wrist|rs|rs_depth | [pick_place_11_11_spot_04](https://huggingface.co/datasets/Purple-SY/pick_place_11_11_spot_04) |
| 2026-11-14 | Left | 3층 | 스팟 1 | `pick_place_11_14_S01_F03_` | 30 | 12,043 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S01_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S01_F03) |
| 2026-11-14 | Left | 3층 | 스팟 2 | `pick_place_11_14_S02_F03` | 30 | 12,938 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S02_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S02_F03) |
| 2026-11-14 | Left | 3층 | 스팟 3 | `pick_place_11_14_S03_F03` | 30 | 13,234 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S03_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S03_F03) |
| 2026-11-14 | Left | 3층 | 스팟 4 | `pick_place_11_14_S04_F03` | 30 | 14,922 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S04_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S04_F03) |
| 2026-11-14 | Left | 3층 | 스팟 5 | `pick_place_11_14_S05_F03` | 30 | 15,101 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S05_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S05_F03) |
| 2026-11-14 | Left | 3층 | 스팟 6 | `pick_place_11_14_S06_F03` | 8 | 4,422 | top|wrist|rs|rs_depth | [pick_place_left_11_14_S06_F03](https://huggingface.co/datasets/Purple-SY/pick_place_left_11_14_S06_F03) |
| 2026-11-17 | Right | 3층 | 스팟 1 | `pick_place_right_11_17_S01_F03_R` | 31 | 16,072 | top|wrist|rs|rs_depth | [pick_place_right_11_17_S01_F03_R](https://huggingface.co/datasets/Purple-SY/pick_place_right_11_17_S01_F03_R) |
| 2026-11-17 ~ 11-18 | Right | 3층 | 스팟 2 | `pick_place_right_11_17_S02_F03_R` | 30 | 14,975 | top|wrist|rs|rs_depth | [pick_place_right_11_17_S02_F03_R](https://huggingface.co/datasets/Purple-SY/pick_place_right_11_17_S02_F03_R) |
| 2026-11-18 ~ 11-19 | Right | 3층 | 스팟 3 | `pick_place_right_11_19_S03_F03_R` | 30 | 16,539 | top|wrist|rs|rs_depth | [pick_place_right_11_19_S03_F03_R](https://huggingface.co/datasets/Purple-SY/pick_place_right_11_19_S03_F03_R) |
| 2026-11-19 | Both | - | -(관절값만, 카메라 없음) | `bimanual/wrist_degrees_side/pick_place_v1` | 1 | 1,504 | 없음 | `bimanual_wrist_degrees_side_pick_place_v1` (HF 비공개) |
| 2026-11-21 | Left | 2층 | S01 | `pick_place_Left_11_21_F02_S01` | 10 | 5,382 | bottom|wrist|top | [pick_place_Left_11_21_F02_S01](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S01) |
| 2026-11-21 | Left | 2층 | S02 | `pick_place_Left_11_21_F02_S02` | 10 | 5,172 | bottom|wrist|top | [pick_place_Left_11_21_F02_S02](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S02) |
| 2026-11-21 | Left | 2층 | S03 | `pick_place_Left_11_21_F02_S03` | 10 | 5,216 | bottom|wrist|top | [pick_place_Left_11_21_F02_S03](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S03) |
| 2026-11-21 | Left | 2층 | S04 | `pick_place_Left_11_21_F02_S04` | 10 | 6,148 | bottom|wrist|top | [pick_place_Left_11_21_F02_S04](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S04) |
| 2026-11-21 | Left | 2층 | S05 | `pick_place_Left_11_21_F02_S05` | 10 | 6,106 | bottom|wrist|top | [pick_place_Left_11_21_F02_S05](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S05) |
| 2026-11-21 | Left | 2층 | S06 | `pick_place_Left_11_21_F02_S06` | 10 | 7,724 | bottom|wrist|top | [pick_place_Left_11_21_F02_S06](https://huggingface.co/datasets/Purple-SY/pick_place_Left_11_21_F02_S06) |
| 2026-11-21 | Left | EX / 1층 | EX | `pick_place_L_11_21_F01_EX` | 5 | 8,793 | bottom|wrist|top | [pick_place_L_11_21_F01_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_21_F01_EX) |
| 2026-11-21 | Left | EX / 2층 | EX | `pick_place_L_11_21_F02_EX` | 5 | 8,427 | bottom|wrist|top | [pick_place_L_11_21_F02_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_21_F02_EX) |
| 2026-11-21 | Left | EX / 3층 | EX | `pick_place_L_11_21_F03_EX` | 5 | 5,474 | bottom|wrist|top | [pick_place_L_11_21_F03_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_21_F03_EX) |
| 2026-11-21 | Right | 1층 | S01 | `pick_place_R_11_21_F01_S01` | 5 | 3,183 | bottom|wrist|top | [pick_place_R_11_21_F01_S01](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S01) |
| 2026-11-21 | Right | 1층 | S02 | `pick_place_R_11_21_F01_S02` | 5 | 3,215 | bottom|wrist|top | [pick_place_R_11_21_F01_S02](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S02) |
| 2026-11-21 | Right | 1층 | S03 | `pick_place_R_11_21_F01_S03` | 5 | 2,997 | bottom|wrist|top | [pick_place_R_11_21_F01_S03](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S03) |
| 2026-11-21 | Right | 1층 | S04 | `pick_place_R_11_21_F01_S04` | 5 | 3,245 | bottom|wrist|top | [pick_place_R_11_21_F01_S04](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S04) |
| 2026-11-21 | Right | 1층 | S05 | `pick_place_R_11_21_F01_S05` | 5 | 3,558 | bottom|wrist|top | [pick_place_R_11_21_F01_S05](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S05) |
| 2026-11-21 | Right | 1층 | S06 | `pick_place_R_11_21_F01_S06` | 5 | 4,252 | bottom|wrist|top | [pick_place_R_11_21_F01_S06](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_S06) |
| 2026-11-21 | Right | 2층 | S01 | `pick_place_R_11_21_F02_S01` | 10 | 7,463 | bottom|wrist|top | [pick_place_R_11_21_F02_S01](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S01) |
| 2026-11-21 | Right | 2층 | S02 | `pick_place_R_11_21_F02_S02` | 10 | 6,547 | bottom|wrist|top | [pick_place_R_11_21_F02_S02](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S02) |
| 2026-11-21 | Right | 2층 | S03 | `pick_place_R_11_21_F02_S03` | 10 | 7,090 | bottom|wrist|top | [pick_place_R_11_21_F02_S03](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S03) |
| 2026-11-21 | Right | 2층 | S04 | `pick_place_R_11_21_F02_S04` | 10 | 6,977 | bottom|wrist|top | [pick_place_R_11_21_F02_S04](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S04) |
| 2026-11-21 | Right | 2층 | S05 | `pick_place_R_11_21_F02_S05` | 10 | 6,840 | bottom|wrist|top | [pick_place_R_11_21_F02_S05](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S05) |
| 2026-11-21 | Right | 2층 | S06 | `pick_place_R_11_21_F02_S06` | 10 | 7,698 | bottom|wrist|top | [pick_place_R_11_21_F02_S06](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_S06) |
| 2026-11-21 | Right | EX / 1층 | EX | `pick_place_R_11_21_F01_EX` | 5 | 10,341 | bottom|wrist|top | [pick_place_R_11_21_F01_EX](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F01_EX) |
| 2026-11-21 | Right | EX / 2층 | EX | `pick_place_R_11_21_F02_EX` | 5 | 9,454 | bottom|wrist|top | [pick_place_R_11_21_F02_EX](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F02_EX) |
| 2026-11-21 | Right | EX / 3층 | EX | `pick_place_R_11_21_F03_EX` | 5 | 8,996 | bottom|wrist|top | [pick_place_R_11_21_F03_EX](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_21_F03_EX) |
| 2026-11-22 | Left | EX / 1층 | EX | `pick_place_L_11_22_F01_EX` | 5 | 9,421 | bottom|wrist|top | `pick_place_L_11_22_F01_EX` (HF 비공개) |
| 2026-11-22 | Left | EX / 2층 | EX | `pick_place_L_11_22_F02_EX` | 5 | 9,028 | bottom|wrist|top | `pick_place_L_11_22_F02_EX` (HF 비공개) |
| 2026-11-22 | Left | EX / 3층 | EX | `pick_place_L_11_22_F03_EX` | 5 | 8,381 | bottom|wrist|top | `pick_place_L_11_22_F03_EX` (HF 비공개) |
| 2026-11-22 | Left | EX / 3층 | EX(TEST) | `pick_place_L_11_22_F03_EX_TEST` | 2 | 4,423 | bottom|wrist|top | `pick_place_L_11_22_F03_EX_TEST` (HF 비공개) |
| 2026-11-22 | Right | EX / 1층 | EX | `pick_place_R_11_22_F01_EX` | 5 | 12,485 | bottom|wrist|top | `pick_place_R_11_22_F01_EX` (HF 비공개) |
| 2026-11-22 | Right | EX / 2층 | EX | `pick_place_R_11_22_F02_EX` | 10 | 18,914 | bottom|wrist|top | `pick_place_R_11_22_F02_EX` (HF 비공개) |
| 2026-11-22 | Right | EX / 3층 | EX | `pick_place_R_11_22_F03_EX` | 5 | 9,681 | bottom|wrist|top | `pick_place_R_11_22_F03_EX` (HF 비공개) |
| 2026-11-23 | Left | 1층 | S01 | `pick_place_L_11_23_F01_S01` | 10 | 4,613 | bottom|wrist|top | [pick_place_L_11_23_F01_S01](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S01) |
| 2026-11-23 | Left | 1층 | S02 | `pick_place_L_11_23_F01_S02` | 10 | 5,225 | bottom|wrist|top | [pick_place_L_11_23_F01_S02](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S02) |
| 2026-11-23 | Left | 1층 | S03 | `pick_place_L_11_23_F01_S03` | 10 | 4,423 | bottom|wrist|top | [pick_place_L_11_23_F01_S03](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S03) |
| 2026-11-23 | Left | 1층 | S04 | `pick_place_L_11_23_F01_S04` | 10 | 4,664 | bottom|wrist|top | [pick_place_L_11_23_F01_S04](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S04) |
| 2026-11-23 | Left | 1층 | S05 | `pick_place_L_11_23_F01_S05` | 10 | 4,708 | bottom|wrist|top | [pick_place_L_11_23_F01_S05](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S05) |
| 2026-11-23 | Left | 1층 | S06 | `pick_place_L_11_23_F01_S06` | 10 | 4,936 | bottom|wrist|top | [pick_place_L_11_23_F01_S06](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_S06) |
| 2026-11-23 | Left | EX / 1층 | EX | `pick_place_L_11_23_F01_EX` | 10 | 14,225 | bottom|wrist|top | [pick_place_L_11_23_F01_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F01_EX) |
| 2026-11-23 | Left | EX / 2층 | EX | `pick_place_L_11_23_F02_EX` | 10 | 12,680 | bottom|wrist|top | [pick_place_L_11_23_F02_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F02_EX) |
| 2026-11-23 | Left | EX / 3층 | EX | `pick_place_L_11_23_F03_EX` | 10 | 11,737 | bottom|wrist|top | [pick_place_L_11_23_F03_EX](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_23_F03_EX) |
| 2026-11-24 | Left | 1층 | S01 | `pick_place_L_11_24_F01_S01` | 2 | 950 | bottom|wrist|top | [pick_place_L_11_24_F01_S01](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_24_F01_S01) |
| 2026-11-24 | Left | 1층 | S03 | `pick_place_L_11_24_F01_S03` | 2 | 839 | bottom|wrist|top | [pick_place_L_11_24_F01_S03](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_24_F01_S03) |
| 2026-11-24 | Left | 1층 | S04 | `pick_place_L_11_24_F01_S04` | 3 | 1,438 | bottom|wrist|top | [pick_place_L_11_24_F01_S04](https://huggingface.co/datasets/Purple-SY/pick_place_L_11_24_F01_S04) |
| 2026-11-24 | Right | 3층 | S04 | `pick_place_R_11_24_F03_S04` | 10 | 8,121 | bottom|wrist|top | [pick_place_R_11_24_F03_S04](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_24_F03_S04) |
| 2026-11-24 | Right | 3층 | S05 | `pick_place_R_11_24_F03_S05` | 11 | 8,651 | bottom|wrist|top | [pick_place_R_11_24_F03_S05](https://huggingface.co/datasets/Purple-SY/pick_place_R_11_24_F03_S05) |
| 2026-11-25 | Right | 3층 | S05 | `pick_place_R_11_25_F03_S05` | 1 | 960 | bottom|wrist|top | `pick_place_R_11_25_F03_S05` (HF 비공개) |

## 4. 합계에서 제외한 자료

| 날짜 | 폴더 | 종류 | Episodes | Frames | HF |
|---|---|---|---|---|---|
| 2026-11-10 | `pick_place_11_10_all` | 합본/가공(원본 별도) | 9 | 10,730 | [pick_place_11_10_all](https://huggingface.co/datasets/Purple-SY/pick_place_11_10_all) |
| 2026-11-10 | `eval/eval_1107_spot02_wrist_hold_20261110_204333` | ACT 평가 실행 기록 | 1 | 422 | [eval_1107_spot02_wrist_hold_20261110_204333](https://huggingface.co/datasets/Purple-SY/eval_1107_spot02_wrist_hold_20261110_204333) |
| 2026-11-10 | `eval/eval_1109_spot01_wrist_hold_20261110_204017` | ACT 평가 실행 기록 | 1 | 426 | [eval_1109_spot01_wrist_hold_20261110_204017](https://huggingface.co/datasets/Purple-SY/eval_1109_spot01_wrist_hold_20261110_204017) |
| 2026-11-10 | `eval/eval_allspots_spot01_wrist_hold_20261110_210333` | ACT 평가 실행 기록 | 1 | 409 | [eval_allspots_spot01_wrist_hold_20261110_210333](https://huggingface.co/datasets/Purple-SY/eval_allspots_spot01_wrist_hold_20261110_210333) |
| 2026-11-10 | `eval/eval_allspots_spot02_wrist_hold_20261110_210513` | ACT 평가 실행 기록 | 1 | 401 | [eval_allspots_spot02_wrist_hold_20261110_210513](https://huggingface.co/datasets/Purple-SY/eval_allspots_spot02_wrist_hold_20261110_210513) |
| 2026-11-10 | `eval/eval_allspots_spot03_wrist_hold_20261110_211149` | ACT 평가 실행 기록 | 1 | 382 | [eval_allspots_spot03_wrist_hold_20261110_211149](https://huggingface.co/datasets/Purple-SY/eval_allspots_spot03_wrist_hold_20261110_211149) |
| 2026-11-10 | `eval/eval_allspots_spot04_wrist_hold_20261110_211325` | ACT 평가 실행 기록 | 1 | 366 | [eval_allspots_spot04_wrist_hold_20261110_211325](https://huggingface.co/datasets/Purple-SY/eval_allspots_spot04_wrist_hold_20261110_211325) |
| 2026-11-14 | `pick_place_diag_S06_20261114_201309` | 진단 녹화 | 1 | 607 | `pick_place_diag_S06_20261114_201309` (HF 비공개) |
| 2026-11-21 | `pick_place_LF02_11_21_wristfix_merged` | 합본/가공(원본 별도) | 60 | 35,748 | `pick_place_LF02_11_21_wristfix_merged` (HF 비공개) |
| 2026-11-22 | `pick_place_R_11_22_EX_seam16` | 합본/가공(원본 별도) | 16 | 32,202 | `pick_place_R_11_22_EX_seam16` (HF 비공개) |

HDD 학습 합본·no_wrist 등 HF 미업로드 파생본은 `data-quality-analysis.md` §6 참고.
