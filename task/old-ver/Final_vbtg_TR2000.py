#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Virtual Ball Toss Game 
# version of 'Cyberball' - https://www.ncbi.nlm.nih.gov/pubmed/16817529
# for PsychoPy (using Python2.7) 

# developed by for use as an fMRI task by the Communication Neuroscience Lab
# original Matlab implementation by Josh Carp
# PsychoPy Python version by Matt O'Donnell (mbod@asc.upenn.edu)

from psychopy import visual, core, logging, event, data, gui
import sys
import random
import csv
import serial
import os
import time

#################
#  PARAMETERS #
#################

maxTime=112          #max time of each round(may change to sinc with scanner)
maxTrials=500        #max number of trials(accumulative of rounds)
holder=1             #player holding the ball
round=1              #flag of rounds
trialCnt=0           #total number of throws(accumulative of rounds)
rndCnt=0             #number of throws in each round
condition="FBALL"

instructions1 = '''
이제 준비가 완료되면 공 던지기 게임을 시작합니다. 잠시만 기다려주세요.
'''

instructions2 = '''
앞에서 연습한 것 처럼 검지 (1번) 버튼을 이용해서 왼쪽 사람에게 공을 던질 수 있고, 중지 (2번) 버튼을 이용해서 오른쪽 사람에게 공을 던질 수 있습니다.
'''

# get subjID
subjDlg = gui.Dlg(title="App Task")
subjDlg.addField('Subject ID:')
subjDlg.addField('Player name:')
subjDlg.addField("Date:")
subjDlg.show()

if gui.OK:
    subj_id=subjDlg.data[0]
    player_name=subjDlg.data[1]
    date=subjDlg.data[2]
else:
    sys.exit()
 
 
players=["최의식 (68) ", "백용천 (75)"]

player1_name = players[0]
player3_name = players[1]

  
################
# Set up images #
################
paths = [d for d in os.listdir('images') if d[1:3]=='to']
throw={}
for p in paths:
    throw[p]=[f for f in os.listdir('images/%s' % p) if f.endswith('.bmp')]

 
################
# Set up window #
################

useFullScreen=False # change to True
win = visual.Window([800,600], monitor="testMonitor", units="deg", allowGUI=False, fullscr=useFullScreen, color="#FFFFFF")


################
# Set up stimuli #
################ 

#TextStim: change height for size
#ImageStim: change size for size

title=visual.TextStim(win,text="Welcome to the Virtual Ball-Tossing Game, an Interactive Task Used for Mental Visualization!", height=0.8, pos=(0,6),color="#000000")
instrText = visual.TextStim(win, text="",height=0.6, color="#000000", wrapWidth=16)
instrKey = visual.TextStim(win, text="", height=0.6, color="#000000", pos=(0,-5))
instr_p1 = visual.TextStim(win, text="",color="#000000", pos=(-6,3), height=0.6, alignHoriz="left")
instr_p2 = visual.TextStim(win, text="",color="#000000", pos=(-6, 0), height=0.6, alignHoriz="left")
instr_p3 = visual.TextStim(win, text="",color="#000000", pos=(-6, -3), height=0.6, alignHoriz="left")
p1_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,3.15), alignHoriz="left")
p3_tick = visual.TextStim(win,text="", color="#000000", pos=(3.5,-2.85), alignHoriz="left")

players = visual.ImageStim(win, image='images/start.bmp', size=(18,10))         #keep ratio 9:5(original 450x250pixel)

round_fix = visual.TextStim(win, text="", height=1.5, color="#000000")

fixation = visual.TextStim(win, text="+", height=2, color="#000000")

goodbye = visual.TextStim(win,text="",color="#000000")

p1name = visual.TextStim(win,text=player1_name,color="#000000", pos=(-7,3), height=0.8)
p2name = visual.TextStim(win,text=player_name,color="#000000", pos=(0,-6), height=0.8)
p3name = visual.TextStim(win,text=player3_name,color="#000000", pos=(7,3), height=0.8)
ready_screen = visual.TextStim(win, text="Ready.....", height=1.2, color="#000000")



def show_instructions():
    title.setAutoDraw(True)
    instrText.setText(instructions1)
    instrText.setAutoDraw(True)
    win.flip()
    #core.wait(20)
    instrKey.setText("PRESS 1 [pointer finger] to continue")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['1'])
    instrText.setText(instructions2)
    win.flip()
    #core.wait(20)
    instrKey.setText("PRESS 2 [middle finger] to begin...")
    instrKey.draw()
    win.flip()
    event.waitKeys(keyList=['2'])
    instrText.setAutoDraw(False)
    
    p1_ticker="."
    p3_ticker="."
    p1_ticker_end=120
    p3_ticker_end=425
    
    title.setText('Joining VBT Game Room')
    instr_p1.setText("PLAYER 1: Wating for player to join")
    instr_p2.setText("PLAYER 2: Welcome %s" % player_name)
    instr_p3.setText("PLAYER 3: Wating for player to join")
    instr_p1.setAutoDraw(True)
    instr_p2.setAutoDraw(True)
    instr_p3.setAutoDraw(True)
    p1_tick.setAutoDraw(True)
    p3_tick.setAutoDraw(True)
    win.flip()
    for tick in range(500):
        if tick == p1_ticker_end:
            instr_p1.setText("PLAYER 1: Welcome %s" % player1_name)
            p1_tick.setAutoDraw(False)
        elif tick == p3_ticker_end:
            instr_p3.setText("PLAYER 3: Welcome %s" % player3_name)
            p3_tick.setAutoDraw(False)
        else:
            if tick % 10 == 0:
                p1_ticker = p1_ticker + "."
                if len(p1_ticker)>6:
                    p1_ticker=""
            if tick % 12 == 0:
                p3_ticker = p3_ticker + "."
                if len(p3_ticker)>6:
                    p3_ticker=""
            if tick < p1_ticker_end:
                p1_tick.setText(p1_ticker)
            if tick < p3_ticker_end:
                p3_tick.setText(p3_ticker)
        win.flip()
    core.wait(2)
    
    title.setAutoDraw(False)
    instr_p1.setAutoDraw(False)
    instr_p2.setAutoDraw(False)
    instr_p3.setAutoDraw(False)
    
def player_names(state=True):
    p1name.setAutoDraw(state)
    p2name.setAutoDraw(state)
    p3name.setAutoDraw(state)

def throw_ball(fromP, toP):
    global trialCnt, holder, rndCnt
    key = "%ito%i" % (fromP,toP)
    
    logging.log(level=logging.DATA, msg="round %i - trial %i - throw: %s - %s" % (round, trialCnt, key, condition))
    
    for s in throw[key]:
        players.setImage('images/%s/%s' % (key,s))
        players.draw()
        win.flip()
        core.wait(0.15)
    
    trialCnt+=1
    rndCnt+=1
    holder=toP
    logging.flush()
    select_throw()              #next throw

def select_throw():
    global condition
    if holder==2:
        logging.log(level=logging.DATA,msg="PLAYER HAS BALL")
        got_ball_time = trialClock.getTime()
        
        choice=[]
        while len(choice)==0 or choice [0] not in ('1','2'):            #until choice(1,2) is made
            core.wait(0.01)
            if trialCnt > maxTrials or trialClock.getTime() > maxTime:
                return
            choice = event.getKeys(keyList=['1','2'])
        if choice[0]=='1':
            throwTo=1
        elif choice[0]=='2':
            throwTo=3
            
        logging.log(level=logging.DATA,msg="PLAYER THROWS TO %i - RT %0.4f" % (throwTo, trialClock.getTime()-got_ball_time))
    else:
        core.wait(random.randint(500,3500)/1000)
    
        if round==2 and rndCnt>8:       #round2 when rndCnt>8(after a few throws)
            condition="UBALL"
            ft=0.5
        elif round==3:                  #round3: always throw to player2
            condition="PBALL"
            ft=-0.5
        else:                           #round1 & round2 when rndCnt<=8(first few throws)
            ft=0.0
        
        throwChoice = random.random() - ft
        if throwChoice < 0.5:           #throw to player 1 or 3
            if holder==1:
                throwTo=3
            else:
                throwTo=1
        else:                           #throw to player 2
            throwTo=2
    
    if trialCnt > maxTrials or trialClock.getTime() > maxTime:
        return
    else:
        throw_ball(holder,throwTo)

# start 

def play_round():
    global rndCnt
    rndCnt=0
    logging.log(level=logging.DATA, msg="Displaying Round %i label" % round)
    round_fix.setText("Round %i" % round)
    round_fix.draw()
    win.flip()
    core.wait(2)
    logging.log(level=logging.DATA, msg="Starting Round %i" % round)
    trialClock.reset()
    players.draw()
    player_names(True)
    win.flip()
    core.wait(0.2)
    select_throw()
    player_names(False)
    fixation.draw()
    win.flip()
    core.wait(2)


# ================================

show_instructions()
ready_screen.setText("OK - here we go!!!")
ready_screen.draw()
win.flip()
event.waitKeys(keyList=['5'])           #for testing

# setup logging #
log_file = logging.LogFile("logs/%s.log" % (subj_id),  level=logging.DATA, filemode="w")

#################
# Trigger scanner #
#################
globalClock = core.Clock()
trialClock = core.Clock()
logging.setDefaultClock(globalClock)

# ADD TRIGGER CODE - 255 on serial port - if scanner is expecting to receive a 'start' trigger
# from task
# some scanners may send a trigger code (i.e. a '5' or a 't') on each TR 
# in which case code here should be adapted (or above where task waits for a space bar to start)
try:
    ser = serial.Serial('/dev/tty.KeySerial1', 9600, timeout=1)
    ser.write('0')
    time.sleep(0.1)
    ser.write('255')
    ser.close()
except:
    print "SCANNER NOT TRIGGERED"
    pass
# end of trigger code

logging.log(level=logging.DATA, msg="START")

# 8 sec disdaq
fixation.setText("+")
fixation.draw()
win.flip()
core.wait(6)

round=1
play_round()

holder=1            #reset holder to 1
round=2
play_round()

holder=1            #reset holder to 1
round=3
play_round()

print("end of exp: %f" %globalClock.getTime())

goodbye.setText("Game Over!\nThanks for playing %s." % player_name)
goodbye.draw()
win.flip()
core.wait(6)     
logging.log(level=logging.DATA, msg="END")          #does not write on log
