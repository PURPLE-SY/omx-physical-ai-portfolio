# ACT 학습 이력

작성: **PURPLE-SY (김승용)**

학습은 별도 GPU PC(집 PC)에서 했다. 이 문서는 노트북에 남은 설정·감사 기록과 외장 HDD의 loss 기록을 근거로 한다. **학습 loss는 실물 성공률이 아니다.** 실물 결과는 physical-validation 문서에 따로 적었다.

## 1. 13,000-step 모델 7종 (2026-11-24 학습, HF 비공개)
**근거:**
- `omx_logs/hf-13k-1124-audit/REPORT.md`, `remote-before.json` → 원격 파일 189개, 8,054,834,770 bytes(약 8.05 GB)
- `verified.json` → 추론 체크포인트 검증 137개 파일, 2,687,955,318 bytes
- HDD `evidence_1121_1124/hf_13k_publication/*/checkpoint_losses.csv` → 1000스텝 단위 train/val loss

**공통 설정:** steps 13000, batch 4, lr 1e-5, chunk 100, seed 1000. 데이터셋 revision은 config에 `None`(로컬 root 사용).

| 모델 (HF Purple-SY/) | 팔·층 | 학습 데이터 | Best (val) | Final 13000 train / val | 파일 / bytes |
|---|---|---|---|---|---|
| omx-act-arm-a-f01-13k-1124 | 오른팔 F01 | pick_place_RF01_11_21_merged | 10000 (0.2584) | 0.19 / 0.2662 | 28 / 1,239,189,634 |
| omx-act-arm-a-f02-13k-1124 | 오른팔 F02 | pick_place_RF02_11_21_merged | 13000 (0.2612) | 0.238 / 0.2612 | 17 / 619,622,657 |
| omx-act-arm-a-f03-13k-1124 | 오른팔 F03 | rf03_1124_qc_merged | 13000 (0.2122) | 0.176 / 0.2122 | 17 / 619,619,195 |
| omx-act-arm-b-f01-13k-1124 | 왼팔 F01 | lf01_1124_qc_merged | 12000 (0.2412) | 0.232 / 0.2434 | 28 / 1,239,194,548 |
| omx-act-arm-b-f02-wristfix-13k-1124 | 왼팔 F02 | pick_place_LF02_11_21_wristfix_merged | 12000 (0.3256) | 0.245 / 0.3526 | 39 / 1,858,761,205 |
| omx-act-arm-a-ex-13k-1124 | 오른팔 EX | r_ex_1124_wristfix | 11000 (0.2835) | 0.204 / 0.2867 | 30 / 1,239,205,923 |
| omx-act-arm-b-ex-13k-1124 | 왼팔 EX | l_ex_1124_wristfix | 12000 (0.3192) | 0.29 / 0.335 | 30 / 1,239,241,608 |
| **합계** | | | | | **189 / 8,054,834,770** |

- arm-b-f02-wristfix에는 물리 비교용 체크포인트 7000(val 0.3338)도 들어 있음
- 학습 큐 로그에 "학습 종료 코드 1"이 한 번 남아 있음(draccus 설정 파싱 오류). 어느 시도인지는 **미확인**. 7종 모두 13000 스텝 체크포인트가 존재함

## 2. 이전 모델
| 모델 | 데이터 | 설정 | 결과 |
|---|---|---|---|
| omx-act-1107-spot02_or-best-20261110 | pick_place_11_07_spot02_OR | 10000 steps, bs 4, lr 1e-5 | best 5500, eval loss 0.261, `robot_success_tested=false` |
| omx-act-1109-01spot-best-20261110 | pick_place_11_09_01spot | – | best 3000, eval loss 0.3361 |
| omx-act-1107-spot01/03–06, spot01_ye | 각 11_07 spot | 미확인 | 미확인 |
| act_pick_place_{L,Left,R}_11_21_* (5종) | 11-21 합본 | 10000 steps, bs 4, lr 1e-5, chunk 100 | loss 값 미추출 |
| omx-left-arm-act-demo-20261126 | pick_place_left_11_14_S02_F03 (ep 0–23 학습, 24–29 held-out) | 13000 steps | F03-002000 val 0.2757 (Best), F03-012000 val 0.2857, Final 013000 val 미확인 |

- `omx-act-pick-place-1110-10k`(공개 모델)의 학습 설정은 **미확인**

## 3. 학습과 실물의 연결
| 모델 | 실물 사용 | 결과 문서 |
|---|---|---|
| arm-b-f01 Best 12000 | B팔 F01 S03 실물 15회 | physical-validation-F01-S03.md |
| arm-b-f02-wristfix Best 12000 | B팔 F02 S05 실물 9회 | physical-validation-F02-S05.md |
| arm-b-ex | 앱 실행 1회(11/26 21:52) | 실행 기록만 있음 |
| arm-b-ex | 손목 명령이 −100 경계를 넘어 보류 | – |
| left-arm-act-demo F03-012000 | 오프라인 근사 시뮬 22/30 | 실물 미실행 |
