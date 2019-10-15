from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from iViewXAPI import *
import numpy as np

'''
Class that starts a simple info routine showing some visual stimulus, 
and either waiting for a keypress to end the routine (manual end),
or waiting a certain amount of time (automatic end)

If both a keypress and a timer are set, the routine can end either manually
on keypress, or when automatically when the timer expires.

@author Patrick Saad
'''

class RoutineInfoFeedback:
    
    has_timer = False
    routine_timer = 0
    win = ""
    win2 = ""
    
    stim_live_pupil = ""
    class_live_pupil = ""
    
    mode = "key"
    key_event = ""
    key_list = []
    components = []
    stimulis = []
    
    def __init__(self, win, win2):
        self.win = win
        self.win2 = win2
        
    def set_timer_duration(self, time_duration):
        self.has_timer = True
        self.routine_timer = core.CountdownTimer()
        self.routine_timer.add(time_duration)
        
    def set_keylist(self, key_list):
        self.key_event = event.BuilderKeyResponse()
        self.key_list = key_list
        
        # Add the key response to the component
        self.components.append(self.key_event)
        
    def set_stimuli_list(self, stimuli_list):
        self.stimulis = stimuli_list
        
        for stimuli in stimuli_list:
            self.components.append(stimuli)
    
    def set_win2_stimulus(self, class_live_pupil, stim_live_pupil):
        self.class_live_pupil = class_live_pupil
        self.stim_live_pupil = stim_live_pupil
    
    def set_win_stimulus(self, class_live_pupil, stim_live_pupil):
        self.class_live_pupil = class_live_pupil
        self.stim_live_pupil = stim_live_pupil
    
    def start(self):
        for thisComponent in self.components:
            if hasattr(thisComponent, 'status'): thisComponent.status = NOT_STARTED

        t = 0
        clock = core.Clock()
        clock.reset()
        frameN = -1
        continueRoutine = True
        endExpNow = False
        while continueRoutine:
            
            # If this routine has a timer and the timer expired, end the routine
            if self.has_timer and self.routine_timer.getTime() <= 0:
                break
            
            # Current time and frame
            t = clock.getTime()
            frameN = frameN + 1
            
            current_pupil_mean = self.class_live_pupil.get_pupil_mean()
            scaling_val = 35
            self.stim_live_pupil.radius = current_pupil_mean * scaling_val
            
            # Draw stimulis
            for stimuli in self.stimulis:
                if t >= 0.0 and stimuli.status == NOT_STARTED:
                    stimuli.tStart = t
                    stimuli.frameNStart = frameN
                    stimuli.setAutoDraw(True)
                    
            # Key Responses
            if len(self.key_list) > 0:
                if t >= 0.0 and self.key_event.status == NOT_STARTED:
                    self.key_event.tStart = t
                    self.key_event.frameNStart = frameN
                    self.key_event.status = STARTED
                    
                    # keyboard checking is just starting
                    event.clearEvents(eventType='keyboard')
                    
                if self.key_event.status == STARTED:
                    theseKeys = event.getKeys(keyList=self.key_list)
                    
                    # check for quit:
                    if "escape" in theseKeys: endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine: break
            
            continueRoutine = False
            
            for component in self.components:
                if hasattr(component, "status") and component.status != FINISHED:
                    continueRoutine = True
                    break
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
            
            # refresh the screen
            if continueRoutine:
                self.win.flip()
                self.win2.flip()
                
        # end while

        # Stop drawing the stimulus
        for component in self.components:
            if hasattr(component, "setAutoDraw"): component.setAutoDraw(False)
            