## VBTG (Virtual Ball Toss Game, Cyberball)
PsychoPy (Python2.7) Version

The code was developed based on the original code from the Communication Neuroscience Lab.
* Original version: Communication Neuroscience Lab, University of Pennsylvania http://cn.asc.upenn.edu, Matt O'Donnell (mbod@asc.upenn.edu)
* Edited version: Clinical Neuroscience Lab, Seoul National University http://www.thecns.snu.ac.kr/, Naeun Oh (nadyaoh5@hanmail.net)

### Instructions
* From standalone PsychoPy IDE
* open `Final_vbtg_TRxxxx.py` and run
* From command line with version of Python2.7 in path with PsychoPy and dependencies installed
* `python Final_vbtg_TRxxxx.py`
* Version set up for MRI scanner environment that waits for start trigger from task. Check comments to alter for a scanner that sends trigger.
* Can read player names and images from external file

### Related Files
* images: images of 3 players throwing a ball
* pimages: 'date_of_exp/player_id', profile images of players by date
* players_list.xlsx: list of players by date, corresponds with players in 'pimages'. You must save data in order as the other two players are assigned as player1 and player3 in that order.
* At the beginning of the experiment, type in 'subj_id' and 'date.' The code will find correspoding images of players.
