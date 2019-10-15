from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from iViewXAPI import *
import numpy as np

class RoutineLivePupilSize:

    ########## Important, variables to reset on each trial loop
    psizeliste = [0]*60000
    psize = 0

    # starting values
    state_no = 0
    state_next = 0
    lmarker = -1
    delay_size = 2

    # filter preferences
    step_limit = 0.09
    lower_th = 1

    # plot settings
    plot_marker = 0
    mean_length = 3
    plot_buffer = 5
    puffer_size = 0
    current_mean = 0
    valid_value = 0
    
    # Must be called outside a while loop (self contained routine with drawing)
    def start(self, win, win2, baseline_inner, baseline_outer):
        t = 0
        clock = core.Clock()
        clock.reset()
        frameN = -1
        continueRoutine = True
        endExpNow = False
        while continueRoutine:
            # Current time and frame
            t = clock.getTime()
            frameN = frameN + 1

            # Get current pupil mean
            current_pupil_mean = self.get_pupil_mean()
            
            scaling = 35

            circle_outer_feedback = visual.Circle(win, edges=96, radius=baseline_outer * scaling, lineWidth=1, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)
            circle_inner_feedback = visual.Circle(win, edges=96, radius=baseline_inner * scaling, lineWidth=1, lineColor=(-0.3 , -0.3, -0.3), fillColor=(-0.3 , -0.3, -0.3), interpolate=True)
            circle_pupil_size_live = visual.Circle(win, edges=96, radius=current_pupil_mean * scaling, lineWidth=4, lineColor=(0,-1,-1), interpolate=True)
            
            circle_outer_feedback1 = visual.Circle(win2, edges=96, radius=baseline_outer * scaling, lineWidth=1, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)
            circle_inner_feedback1 = visual.Circle(win2, edges=96, radius=baseline_inner * scaling, lineWidth=1, lineColor=(-0.3 , -0.3, -0.3), fillColor=(-0.3 , -0.3, -0.3), interpolate=True)
            circle_pupil_size_live1 = visual.Circle(win2, edges=96, radius=current_pupil_mean * scaling, lineWidth=4, lineColor=(0,-1,-1), interpolate=True)
        
            circle_outer_feedback1.setAutoDraw(True)
            circle_inner_feedback1.setAutoDraw(True)
            circle_pupil_size_live1.setAutoDraw(True)
            
            circle_outer_feedback.setAutoDraw(True)
            circle_inner_feedback.setAutoDraw(True)
            circle_pupil_size_live.setAutoDraw(True)
            
           
           
            continueRoutine = True
            
            # check if all components have finished
            # if not continueRoutine:  break
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                continueRoutine = False
            
            # refresh the screen
            if continueRoutine: win.flip()
            if continueRoutine: win2.flip()
        
        #circle_outer_feedback1.setAutoDraw(False)
        #circle_inner_feedback1.setAutoDraw(False)
        #circle_pupil_size_live1.setAutoDraw(False)
        
        #circle_outer_feedback.setAutoDraw(False)
        #circle_inner_feedback.setAutoDraw(False)
        #circle_pupil_size_live.setAutoDraw(False)
        
                
    # Must be called in a while loop (just getting the pupil value for every frame in a while loop)
    def get_pupil_mean(self):
        
        # Eye-tracker data
        res = iViewXAPI.iV_GetSample(byref(sampleData))
        psize = (sampleData.leftEye.diam) # /32 fur highspeed eyetracker, ohne /32 fur RED

        #--------------------
        # State 0: starting

        if self.state_no == 0:

            if self.lmarker < 1:
            
                self.lmarker = self.lmarker + 1
                self.psizeliste[self.lmarker] = psize
                
                self.state_next = 0
         
            else:
            
                if psize > self.lower_th and self.psizeliste[self.lmarker] > self.lower_th and self.psizeliste[self.lmarker-1] > self.lower_th and (abs(psize-self.psizeliste[self.lmarker]) <= self.step_limit) and (abs(self.psizeliste[self.lmarker]-self.psizeliste[self.lmarker-1]) <= self.step_limit):
                    self.lmarker = self.lmarker + 1
                    self.psizeliste[self.lmarker] = psize
                    
                    self.state_next = 1
                
                else:
                    self.psizeliste[self.lmarker-1] = self.psizeliste[self.lmarker]
                    self.psizeliste[self.lmarker] = psize
                    
                    self.state_next = 0
            
        #----------------------
        # State 1: observation
        if self.state_no == 1:
            self.plot_marker = 1 
            
            # Filter Activation
            #- - - - - - - - - - -
            if psize <= self.lower_th:
                on = 1
                jump_marker = self.lmarker + 1 # marks values to be replaced 
                
                # Identification of last self.valid_value before the blink
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                while on == 1:
                    if self.psizeliste[self.lmarker] >= self.lower_th and self.psizeliste[self.lmarker-1] >= self.lower_th and self.psizeliste[self.lmarker-2] >= self.lower_th and abs(self.psizeliste[self.lmarker]-self.psizeliste[self.lmarker-1]) <= self.step_limit and abs(self.psizeliste[self.lmarker-1]-self.psizeliste[self.lmarker-2]) <= self.step_limit:
                        self.valid_value = self.psizeliste[self.lmarker]
                        self.lmarker = self.lmarker + 1
                        
                        # replacing values
                        for i in range(self.lmarker, jump_marker, 1):
                            self.psizeliste[i] = self.valid_value
                        
                        self.psizeliste[jump_marker] = self.valid_value
                        self.lmarker = jump_marker
                        self.puffer_size = jump_marker + self.delay_size
                        on = 0
                        self.state_next = 2
                    else:
                        self.lmarker = self.lmarker-1
            
            else:
                self.lmarker = self.lmarker + 1
                self.psizeliste[self.lmarker] = psize
                self.state_next = 1

        #-------------------------------------------------------------
        # State 2: identification of next self.valid_value after the blink
        if self.state_no == 2:
            self.plot_marker = 1
            # collecting values following the blink
            
            if self.lmarker < self.puffer_size:
                self.lmarker = self.lmarker + 1
                self.psizeliste[self.lmarker] = psize
                
                self.state_next = 2

            else:
                # identification of next self.valid_value after the blink
                if psize > self.lower_th and abs(psize-self.psizeliste[self.lmarker]) <= self.step_limit and abs(self.psizeliste[self.lmarker]-self.psizeliste[self.lmarker-1]) <= self.step_limit:               
                    self.lmarker = self.lmarker + 1
                    self.psizeliste[self.lmarker] = psize
                    
                    self.state_next = 1
                else:
                   self.lmarker = self.lmarker + 1
                   self.psizeliste[self.lmarker] = psize
                   self.psizeliste[self.lmarker-2] = self.valid_value
                   
                   self.state_next = 2

        #- - - - - - - - - - - - - - - - - - - - - - - - - - -
        # smooth & plot data:
        if self.state_no == 0 or self.state_no == 1 or self.state_no == 2:

            if self.plot_marker == 1:
                # BASELINE RINGE (schwarz): MW +/-SD
                #- - - - - - - - - - - - - - - - - - - -
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -     
                # FEEDBACK RINGE (rot | grau): Pupillengroesse u. Extrema
                #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if self.lmarker >= self.mean_length + self.plot_buffer:
                    self.current_mean = 0
                    
                    for p in range(1, self.mean_length+1, 1):
                        self.current_mean = self.psizeliste[self.lmarker-p-self.plot_buffer] + self.current_mean
                        
                    self.current_mean = (self.current_mean/self.mean_length)

        ############################################################################

        # Important
        self.state_no = self.state_next

        return self.current_mean