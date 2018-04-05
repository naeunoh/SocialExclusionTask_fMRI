# SocialExclusionTask_fMRI
Task-fMRI using cyberball in the SSK project

## VBTG (Virtual Ball Toss Game)
PsychoPy (Python2.7) Version
* Communication Neuroscience Lab, University of Pennsylvania http://cn.asc.upenn.edu
* Matt O'Donnell (mbod@asc.upenn.edu)
Edited for use by the Clinical Neuroscience Lab, Seoul National University http://thecns.snu.ac.kr
* Naeun Oh

### Instructions
* From standalone PsychoPy IDE
* open `Final_vbtg_TR2000.py` and run
* From command line with version of Python2.7 in path with PsychoPy and dependencies installed
* `python Final_vbtg_TR2000.py`
* Version set up for scanner environment that waits for start trigger from task. Check comments to alter for a scanner that sends trigger.

### Related Files & Folders
images: images of 3 players throwing a ball
pimages: 'date_of_exp\player_id', profile images of players by date of experiment
players_list.xlsx: list of players by date of experiment, corresponds with players in 'pimages', must save data in order, 자신을 제외하고 저장된 순서대로 player1, player3로 배정됨.

=> 실험 시작할 때 입력하는 subj_id, date로 player image와 나머지 player들이 결정됨. 코드 직접 수정 불필요!
