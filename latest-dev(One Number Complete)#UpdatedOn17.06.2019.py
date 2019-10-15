#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.90.1),
    on April 23, 2019, at 11:05
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np

from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import random
import os
import sys
import math
import copy
from random import shuffle
from psychopy.tools.monitorunittools import posToPix
from psychopy import visual, core
import numpy

from modules.iViewXAPI import  *
from modules.routine_info import RoutineInfo
from modules.routine_info_feedback import RoutineInfoFeedback
from modules.routine_baseline import RoutineBaseline
from modules.routine_live_pupil_size import RoutineLivePupilSize

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Simon-task'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])

dir_experiment = _thisDir + os.sep

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

#Setup the Window
win = visual.Window(
    size=[1000, 1000], fullscr=True, screen=2,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor', color=[-0.3,-0.3,-0.3], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
    
win2 = visual.Window(
    size=[1000, 1000], fullscr=True, screen=1,
    allowGUI=True, allowStencil=False,
    monitor='testMonitor2', color=[-0.3,-0.3,-0.3], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# ---------------------------------------------
#---- connect to iViewX
# ---------------------------------------------
res = iViewXAPI.iV_SetLogger(c_int(1), c_char_p("logs/logs.txt"))
res = iViewXAPI.iV_Connect(c_char_p('141.54.159.23'), c_int(4444), c_char_p('141.54.159.21'), c_int(5555))

res = iViewXAPI.iV_GetSystemInfo(byref(systemData))
print "iV_GetSystemInfo: " + str(res)
print "Samplerate: " + str(systemData.samplerate)
print "iViewX Version: " + str(systemData.iV_MajorVersion) + "." + str(systemData.iV_MinorVersion) + "." + str(systemData.iV_Buildnumber)
print "iViewX API Version: " + str(systemData.API_MajorVersion) + "." + str(systemData.API_MinorVersion) + "." + str(systemData.API_Buildnumber)


    
text_2 = visual.TextStim(win=win, name='text_2',
    text='Baseline Registration will be made now. Press any key to start.',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
    
baseline_text_in_loop = visual.TextStim(win=win, name='baseline_text_in_loop',
    text='test',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
    
baselineClock = core.Clock()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()



# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

########## 
# Baseline instructions

keylist = ["space"]
stim1 = visual.TextStim(
    win=win,
    name='stim1',
    text='Baseline Registration will be made now. Press space key to start.',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

routine = RoutineInfo(win)
routine.set_stimuli_list( [stim1] )
routine.set_keylist(keylist)
routine.start()
########################

###################################
# Routine: Baseline

timer_duration = 3
routine = RoutineBaseline(win)
routine.set_timer_duration(timer_duration)
routine.start()

# Get the baseline values after the routine is done
baseline_vals = routine.get_baseline_vals()
baseline_mean = routine.get_baseline_mean()
baseline_sd = routine.get_baseline_sd()
baseline_inner = routine.get_inner_baseline_val()
baseline_outer = routine.get_outer_baseline_val()
        
# Save the data
iViewXAPI.iV_StopRecording()
iViewXAPI.iV_SaveData(str(dir_experiment + expName + expInfo['participant'] + '_baseline'), str(), str(),1)
thisExp.addData('baseline_vals', baseline_vals)
thisExp.addData('baseline_mean', baseline_mean)
thisExp.addData('baseline_sd', baseline_sd)
    
########## 
# Instructions 2

keylist = ["space"]
stim1 = visual.TextStim(
    win=win,
    name='stim1',
    text='Use Up or Down key according to their value! \nUp if number higher than 5 Or\nDown if number lower than 5 \nPress space key to start. \n',
    font='Arial',
    units='pix', pos=[0, 0], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

routine = RoutineInfo(win)
routine.set_stimuli_list( [stim1] )
routine.set_keylist(keylist)
routine.start()
########################

# set up handler to look after randomisation of etc
trials = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditionstest.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))


        
trialClock = core.Clock()
target = visual.TextStim(win=win, name='target',
    text='default text',
    font='Arial',
    pos=[0,0], height=100, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

trialFinishedClock = core.Clock()
trial_finished = visual.TextStim(win=win, name='trial_finished',
    text='Thanks for your participation.\nPress any key to finish the trial.',
    font='Arial',
    pos=(0, 0), height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
    
scaling_val = 35
circle_inner_feedback = visual.Circle(win2, edges=96, radius=baseline_inner * scaling_val, lineWidth=1, lineColor=(-0.3 , -0.3, -0.3), fillColor=(-0.3 , -0.3, -0.3), interpolate=True)
circle_outer_feedback = visual.Circle(win2, edges=96, radius=baseline_outer * scaling_val, lineWidth=1, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)
circle_pupil_size_live = visual.Circle(win2, edges=96, radius=0, lineWidth=4, lineColor=(0,-1,-1), interpolate=True)

#circle_inner_feedback = visual.Circle(win, edges=96, radius=baseline_inner * scaling_val, lineWidth=1, lineColor=(-0.3 , -0.3, -0.3), fillColor=(-0.3 , -0.3, -0.3), interpolate=True)
#circle_outer_feedback = visual.Circle(win, edges=96, radius=baseline_outer * scaling_val, lineWidth=1, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)
#circle_pupil_size_live = visual.Circle(win, edges=96, radius=0, lineWidth=4, lineColor=(0,-1,-1), interpolate=True)

loop_counter = 0
# stim trial counter
stim_counter = visual.TextStim(
    win=win,
    name='stim_counter',
    text= "Qustions answered: "+ str(loop_counter) + " / " + str(len(trials.trialList)),
    font='Arial',
    units='pix', pos=[300, 300], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
 

loop_counter_truth = 0 
# stim truth counter
stim_truth = visual.TextStim(
    win=win,
    name='stim_truth',
    text="Truth told: " + str(loop_counter_truth) + " / " + str(len(trials.trialList)),
    font='Arial',
    units='pix', pos=[300, 270], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
 
loop_counter_lie = 0 
# stim lie counter
stim_lie = visual.TextStim(
    win=win,
    name='stim_lie',
    text="Lies told: " + str(loop_counter_lie) + " / " + str(len(trials.trialList)),
    font='Arial',
    units='pix', pos=[300, 240], height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0); 
 
response_counter1=0 
# stim user response counter    
stim_user_response = visual.TextStim(
    win=win2,
    name='stim_user_response',
    text="Waiting...",
    font='Arial',
    units='pix', pos=[300, 300], height=50, wrapWidth=None, ori=0, 
    color='yellow', colorSpace='rgb', opacity=1,
    depth=-1.0);

for thisTrial in trials:
    currentLoop = trials
    
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "trial"-------
    
    # Live pupil class for window 2
    class_live_pupil = RoutineLivePupilSize()
    
    t = 0
    trialClock.reset()
    frameN = -1
    continueRoutine = True
    
    # Target text
    target.setColor("white") # reset colors
    target.setText(arrowDirec)
    target.setPos(position)
    
    key_response = event.BuilderKeyResponse()
    
    # keep track of which components have finished
    trialComponents = [target, key_response, stim_counter, stim_truth, stim_lie]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    while continueRoutine:
        t = trialClock.getTime()
        frameN = frameN + 1
        
        # *target* updates
        if t >= 0.0 and target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart = t
            target.frameNStart = frameN  # exact frame index
            target.setAutoDraw(True)
        frameRemains = 0.0 + 300- win.monitorFramePeriod * 0.75  # most of one frame period left
        
        if target.status == STARTED and t >= frameRemains: target.setAutoDraw(False)
        
        # stim counter
        if t >= 0.0 and stim_counter.status == NOT_STARTED:
            # keep track of start time/frame for later
            stim_counter.tStart = t
            stim_counter.frameNStart = frameN  # exact frame index
            stim_counter.setAutoDraw(True)
        
        if stim_counter.status == STARTED and t >= frameRemains: stim_counter.setAutoDraw(False)
        
        # stim truth
        if t >= 0.0 and stim_truth.status == NOT_STARTED:
            # keep track of start time/frame for later
            stim_truth.tStart = t
            stim_truth.frameNStart = frameN  # exact frame index
            stim_truth.setAutoDraw(True)
        
        if stim_truth.status == STARTED and t >= frameRemains: stim_truth.setAutoDraw(False)
        
        # stim lie
        if t >= 0.0 and stim_lie.status == NOT_STARTED:
            # keep track of start time/frame for later
            stim_lie.tStart = t
            stim_lie.frameNStart = frameN  # exact frame index
            stim_lie.setAutoDraw(True)
        
        if stim_lie.status == STARTED and t >= frameRemains: stim_lie.setAutoDraw(False)
        
        # stim_user_response
        if t >= 0.0 and stim_user_response.status == NOT_STARTED:
            stim_user_response.tStart = t
            stim_user_response.frameNStart = frameN  # exact frame index
            stim_user_response.setAutoDraw(True)
        
        if stim_user_response.status == STARTED and t >= frameRemains: stim_user_response.setAutoDraw(False)
        
        
        # Draw pupil feedback
        current_pupil_mean = class_live_pupil.get_pupil_mean()
        circle_pupil_size_live.radius = current_pupil_mean * scaling_val
        circle_outer_feedback.setAutoDraw(True)
        circle_inner_feedback.setAutoDraw(True)
        circle_pupil_size_live.setAutoDraw(True)
        ###
        
        # Keys
        if t >= 0 and key_response.status == NOT_STARTED:
            key_response.tStart = t
            key_response.frameNStart = frameN
            key_response.status = STARTED
            win.callOnFlip(key_response.clock.reset)
            event.clearEvents(eventType='keyboard')
        
        
        if key_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['up', 'down'])
            
            # check for quit:
            if "escape" in theseKeys: endExpNow = True
            
            # at least one key was pressed
            if len(theseKeys) > 0:
                key_response.keys = theseKeys[-1]
                key_response.rt = key_response.clock.getTime()
                
                if str(key_response.keys) =="up":
                    response_counter1 += 1
                    stim_user_response.text = "Higher " + str(response_counter1) + " / " + str(len(trials.trialList))
                
                else:
                    response_counter1 += 1
                    stim_user_response.text = "Lower " + str(response_counter1) + " / " + str(len(trials.trialList))
                # if key is correct key for this question
                if key_response.keys == str(corrAns):
                    key_response.corr = 1
                    target.setColor('green')
                    
                else:
                    key_response.corr = 0
                    target.setColor('red')
                
                # End the routine
                continueRoutine = False
        
        frameRemains = 0.0 + 300- win.monitorFramePeriod * 0.75  # most of one frame period left
        if key_response.status == STARTED and t >= frameRemains:
            key_response.status = STOPPED
            
            
        # check if all components have finished
        if not continueRoutine: break
            
        continueRoutine = False  # will revert to True if at least one component still running
        
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
        
        # refresh the screens
        if continueRoutine:
            win.flip()
            win2.flip()
    #Counter for Questions Remaining        
    
    loop_counter += 1
    stim_counter.text ="Qustions answered: " + str(loop_counter) + " / " + str(len(trials.trialList))
    
    #Counter for truth
    if len(theseKeys) > 0:
        key_response.keys = theseKeys[-1]
        key_response.rt = key_response.clock.getTime()
        if (key_response.keys == str(corrAns)) or (key_response.keys == corrAns):
            loop_counter_truth += 1
            stim_truth.text ="Truth told: " + str(loop_counter_truth) + " / " + str(len(trials.trialList))
        else:
            loop_counter_lie += 1
            stim_lie.text ="Lies told: " + str(loop_counter_lie) + " / " + str(len(trials.trialList))
    
    ############################
    # Routine Pause
    timer_duration = 6
    routine = RoutineInfoFeedback(win, win2)
    routine.set_win2_stimulus(class_live_pupil, circle_pupil_size_live)
    routine.set_stimuli_list( [target, stim_counter, stim_truth, stim_lie] )
    routine.set_timer_duration(timer_duration)
    routine.start()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # Save user response
    trials.addData('response.keys', key_response.keys)
    trials.addData('response.corr', key_response.corr)
    
    
    thisExp.nextEntry()
# end while

circle_inner_feedback.setAutoDraw(False)
circle_outer_feedback.setAutoDraw(False)
circle_pupil_size_live.setAutoDraw(False)

################################
# Bye 2
keylist = ["space"]
routine = RoutineInfo(win)
routine.set_stimuli_list( [trial_finished] )
routine.set_keylist(keylist)
routine.start()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
win2.close()
core.quit()
