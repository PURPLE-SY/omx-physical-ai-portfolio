import json,shutil
from pathlib import Path
out=Path('/home/purple/omx_logs/hf-13k-1124-audit');rs=json.loads((out/'verified.json').read_text())
lines=['# ACT 13k 1124 다운로드 및 무결성 확인','', '모터/카메라 연결, 추론, 재학습은 수행하지 않음. A팔 ID12 문제 해결 및 별도 승인 전 실물 실행 금지. 기존 모델·Auto Homing 브랜치 변경 없음.','', '## 범위','원격 revision을 고정해 추론 패키지와 평가·품질 기록을 다운로드. training_state(optimizer/RNG 등)는 재학습용이라 제외. 기존 omx_models 및 해당 HF 캐시에서 이번 7종의 사전 저장본을 찾지 못함. 구형 10k 및 cpu-compat 모델은 보존.','', '## 체크포인트 및 학습 데이터','|모델|Best|Final|추가|학습 dataset repo|','|---|---:|---:|---:|---|']
for r in rs:
 roles=r['evaluation']['roles'];c=r['checkpoints'][-1]
 lines.append(f"|{r['repo'].split('/')[-1]}|{roles['best']}|{roles['final']}|{roles.get('physical_comparison','—')}|{c['dataset']['repo_id']}|")
lines+=['','## 파일 검증','원격 LFS SHA-256과 크기를 사전 기록. 다운로드 후 1MiB 스트리밍 해시로 비교. 일반 Git 파일은 원격 blob SHA-1도 검증하고 SHA-256을 별도 기록. 제공된 SHA256SUMS의 다운로드 대상 항목도 비교. SHA256SUMS 자신 등 manifest 미포함 파일은 원격 Git blob으로 검증. 전체 파일별 값은 verified.json, 원격 사전 정보는 remote-before.json에 보존.','']
for r in rs:
 lines+=['### '+r['repo'],f"- 위치: `{r['path']}`",f"- revision: `{r['revision']}`",f"- 검증 파일: {len(r['files'])}; 총 {sum(x['size'] for x in r['files'])} bytes"]
 for c in r['checkpoints']:
  cameras={k:v['shape'] for k,v in c['input_features'].items() if 'images' in k}
  lines += [f"- {c['step']}: 필수 파일 누락 {c['missing']}; 카메라 {cameras}; state/action 6; chunk {c['chunk_size']}; device {c['device']}"]
 lines += [f"- 학습 시 root: `{r['checkpoints'][-1]['dataset']['root']}`",f"- 학습 dataset revision: `{r['checkpoints'][-1]['dataset'].get('revision')}`",f"- 평가 기록 관절 순서: {r['evaluation'].get('offline_action_metrics',{}).get('joint_names','미기재')}"]
lines+=['','## 실행 전 남은 확인','파일 무결성 통과는 실물 실행 안전성이나 설치된 LeRobot과의 호환성 검증이 아님. 모델 가중치를 로드하거나 ACT 추론하지 않음. CUDA 설정은 CPU 노트북에서 추후 승인된 실행 시 별도 device 선택 검토 필요. 카메라 키/해상도는 확인했으나 실제 USB serial·색상/좌표·작업대 배치는 확인하지 않음. 관절의 실물 ID·단위·캘리브레이션·손목 턴/보정과 현재 장치의 일치도 추가 확인 필요. 누락된 외부 보정 파일을 자동 생성하거나 안전 관문을 해제하지 않음.','',f"검증 완료 저장소 {len(rs)}; 추론 체크포인트 {sum(len(r['checkpoints']) for r in rs)}; 현재 여유 {shutil.disk_usage('/home/purple/omx_models').free} bytes."]
(out/'REPORT.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[:18]))
