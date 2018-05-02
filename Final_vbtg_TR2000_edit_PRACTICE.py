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

# edited for use by the Clinical Neuroscience Lab

import xlrd
from psychopy import visual, core, logging, event,data, gui
import sys
import random
import csv
import serial
import os
import time
from psychopy.preferences import prefs
prefs.general['shutdownKey']='q'

#################
#  PARAMETERS #
#################

maxTime=20          #max time of each round(may change to sinc with scanner)    112
maxTrials=500        #max number of trials(accumulative of rounds)
holder=1             #player holding the ball
round=1              #flag of rounds
trialCnt=0           #total number of throws(accumulative of rounds)
rndCnt=0             #number of throws in each round
condition="FBALL"
def_font="Arial"


instructions1 = '''
지금은 연습게임입니다.
'''

instructions2 = '''
   검지 (1번) 버튼을 이용해서 왼쪽 사람에게 공을 던질 수 있고,\n
중지 (2번) 버튼을 이용해서 오른쪽 사람에게 공을 던질 수 있습니다.
'''

# get subjID
subjDlg = gui.Dlg(title="App Task")
subjDlg.addField('Player name:')
subjDlg.show()

if gui.OK:
    player_name=subjDlg.data[0]
else:
    print('User cancelled')
    core.quit()
    sys.exit()

################
#Set up players 
################

player1_name="컴퓨터 1"
player3_name="컴퓨터 2"


################
# Set up images #
################

#image of throws
paths = [d for d in os.listdir('images') if d[1:3]=='to']
throw={}
for p in paths:
    throw[p]=[f for f in os.listdir('images/%s' % p) if f.endswith('.bmp')]

#image of players
paths2 = [d for d in os.listdir('pimages/practice')]
count=0
for p in paths2:
    if count==0:    #first image
            p1=p
            count=count+1
    elif count==1:  #third image
            p3=p
            count=count+1


################
# Set up window #
################

useFullScreen=False # change to True
win = visual.Window([1200,900], monitor="testMonitor", units="deg", allowGUI=False, fullscr=useFullScreen, color="#FFFFFF")

################
# Set up stimuli #
################ 

#TextStim: change height for size
#ImageStim: change size for size
title=visual.TextStim(win,text="가상 공 던지기 게임에 오신 것을 환영합니다!", height=1.0, pos=(0,6),color="#000000", wrapWidth=30, font=def_font)
instrText = visual.TextStim(win, text="",height=0.6, color="#000000", wrapWidth=25, font=def_font)

#instrTextBox= visual.TextBox(window=win, text="", font_size=18, font_color=(0,0,0), line_spacing=1, line_spacing_units='pix', grid_horz_justification="center")

instr_p1 = visual.TextStim(win, text="",color="#000000", pos=(-6,3), height=0.6, alignHoriz="left", font=def_font)
#instr_p1_name = visual.TextStim(win, text="",color="#000000", pos=(-3.6,3), height=0.6, alignHoriz="left", font=def_font, bold=True)       for bold names
instr_p2 = visual.TextStim(win, text="",color="#000000", pos=(-6, 0), height=0.6, alignHoriz="left", font=def_font)
instr_p3 = visual.TextStim(win, text="",color="#000000", pos=(-6, -3), height=0.6, alignHoriz="left", font=def_font)

p1_tick = visual.TextStim(win,text="", color="#000000", pos=(2.5,3.15), alignHoriz="left")
p3_tick = visual.TextStim(win,text="", color="#000000", pos=(2.5,-2.85), alignHoriz="left")

players = visual.ImageStim(win, image='images/start.bmp', size=(18,10))         #keep ratio 9:5(original 450x250pixel)

round_fix = visual.TextStim(win, text="", height=2, color="#000000", font=def_font)

fixation = visual.TextStim(win, text="+", height=2, color="#000000")
 
p1name = visual.TextStim(win,text=player1_name,color="#000000", pos=(-9,3), height=0.8,font=def_font)
p2name = visual.TextStim(win,text=player_name,color="#000000", pos=(0,-6), height=0.8, font=def_font)
p3name = visual.TextStim(win,text=player3_name,color="#000000", pos=(9,3), height=0.8, font=def_font)

p1image = visual.ImageStim(win, image='pimages/practice/p1', pos=(-9,7), size=(5,5)) 
p3image = visual.ImageStim(win, image='pimages/practice/p3', pos=(9,7), size=(5,5)) 

ready_screen = visual.TextStim(win, height=1.2, color="#000000", font=def_font)
goodbye = visual.TextStim(win,text="",color="#000000", font=def_font)



def show_instructions():
    title.setAutoDraw(True)
    instrText.setText(instructions1)
    instrText.setAutoDraw(True)
    win.flip()
    core.wait(5)
    instrText.setText(instructions2)
    win.flip()
    core.wait(7)
    instrText.setAutoDraw(False)
    
    title.setAutoDraw(False)
    instr_p1.setAutoDraw(False)
    instr_p2.setAutoDraw(False)
    instr_p3.setAutoDraw(False)
    
def player_profiles(state=True):
    p1name.setAutoDraw(state)
    p2name.setAutoDraw(state)
    p3name.setAutoDraw(state)
    p1image.setAutoDraw(state)
    p3image.setAutoDraw(state)
    


def throw_ball(fromP, toP):
    global trialCnt, holder, rndCnt
    key = "%ito%i" % (fromP,toP)
    
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
            
    else:
        core.wait(random.randint(500,3500)/1000)
    
        if round==2 and rndCnt>5:      #round2 when rndCnt>5(after a few throws)
            condition="UBALL"
            ft=0.5
        elif round==3 and rndCnt>5:    #round3 when rndCnt>5(after a few throws): throw to player2
            condition="PBALL"
            ft=-0.5
        else:                           #round1 all, round2 and round3 when rndCnt<=5(first few throws)
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
    round_fix.setText("%i회" % round)
    round_fix.draw()
    win.flip()
    core.wait(2)
    trialClock.reset()
    players.draw()
    player_profiles(True)
    win.flip()
    core.wait(0.2)
    select_throw()
    player_profiles(False)
    fixation.draw()
    win.flip()
    core.wait(2)


# ================================

show_instructions()
ready_screen.setText("게임을 시작합니다!")
ready_screen.draw()
win.flip()
event.waitKeys(keyList=['5'])           #for testing

globalClock = core.Clock()
trialClock = core.Clock()
logging.setDefaultClock(globalClock)

# 8 sec disdaq
fixation.setText("+")
fixation.draw()
win.flip()
core.wait(6)

round=1
play_round()

goodbye.setText(" 게임이 끝났습니다!\n%s님 감사합니다." % player_name)
goodbye.draw()
win.flip()
core.wait(6)     
core.quit()
sys.exit()