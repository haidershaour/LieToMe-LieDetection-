from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from iViewXAPI import  *
import numpy as np

'''
Class that starts a baseline measuring routine with two black crosses in the middle.
The final baseline values, baseline mean, baseline standard deviation can be obtained
via get functions.

@author Patrick Saad
'''

class RoutineBaseline:

    routine_timer = ""
    win = ""
        
    baseline_vals = [0]*1900 # ca. 900 bei 30Hz | ca. 1900 bei 60Hz
    current_baseline_val = 0

    # starting values
    state_no = 0
    lmarker = -1
    valid_value = 0
    delay_size = 2
    
    puffer_size = 0
    jump_marker = 0

    # filter preferences
    step_limit = 0.19    # 30Hz: 0.19 | 60Hz: 0.09
    lower_th = 2
    
    def __init__(self, win):
        self.win = win
        
    def set_timer_duration(self, time_duration):
        self.routine_timer = core.CountdownTimer()
        self.routine_timer.add(time_duration)
        
    def get_baseline_vals(self):
        self.baseline_vals = filter(None, self.baseline_vals)
        return self.baseline_vals
        
    def get_baseline_mean(self):
        return round((sum(self.baseline_vals)/(len(self.baseline_vals))),2)
        
    def get_baseline_sd(self):
        return abs(round(np.std(self.baseline_vals),8))
    
    def get_percent_change(self):
        sd = self.get_baseline_sd()
        mean = self.get_baseline_mean()
        return round((sd/mean),2)
    
    # computing aussenringradius - maximum deviation 
    def get_outer_baseline_val(self):
        mean = self.get_baseline_mean()
        percent_change = self.get_percent_change()
        
        return mean+(mean*percent_change)

    # computing innenringradius - minimum deviation
    def get_inner_baseline_val(self):
        mean = self.get_baseline_mean()
        percent_change = self.get_percent_change()
        
        return mean-(mean*percent_change)
        
    def start(self):
        
        #######
        iViewXAPI.iV_StartRecording()

        t = 0
        baselineClock = core.Clock()
        baselineClock.reset()
        frameN = -1
        continueRoutine = True
        endExpNow = False
        while continueRoutine and self.routine_timer.getTime() > 0:
            # Current time and frame
            t = baselineClock.getTime()
            frameN = frameN + 1
            
            # API Call
            # Collect pupil eye diameter
            res = iViewXAPI.iV_GetSample(byref(sampleData))
            self.current_baseline_val = (sampleData.leftEye.diam) # /32 fur highspeed eyetracker, ohne /32 fur RED
            
            # The following if statements remove blinks, etc. Use as is
            
            #--------------------
            # state 0: starting
            #--------------------
            if self.state_no == 0:
                if self.lmarker < 1:
                    self.lmarker = self.lmarker + 1
                    self.baseline_vals[self.lmarker] = self.current_baseline_val
                    self.state_next = 0
             
                else:
                    if self.current_baseline_val > self.lower_th and self.baseline_vals[self.lmarker] > self.lower_th and self.baseline_vals[self.lmarker-1] > self.lower_th and (abs(self.current_baseline_val-self.baseline_vals[self.lmarker]) <= self.step_limit) and (abs(self.baseline_vals[self.lmarker]-self.baseline_vals[self.lmarker-1]) <= self.step_limit):
                        self.lmarker = self.lmarker + 1
                        self.baseline_vals[self.lmarker] = self.current_baseline_val
                        self.state_next = 1
                    else:
                        self.baseline_vals[self.lmarker-1] = self.baseline_vals[self.lmarker]
                        self.baseline_vals[self.lmarker] = self.current_baseline_val

                        self.state_next = 0

            #----------------------
            # state 1: observation
            #----------------------
            if self.state_no == 1:

                # Filter Activation
                #- - - - - - - - - - -
                if self.current_baseline_val <= self.lower_th:
                    on = 1
                    self.jump_marker = self.lmarker + 1 # marks values to be replaced 
              
                    # Identification of last self.valid_value before the blink
                    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    while on == 1:
                        if self.baseline_vals[self.lmarker] >= self.lower_th and self.baseline_vals[self.lmarker-1] >= self.lower_th and self.baseline_vals[self.lmarker-2] >= self.lower_th and abs(self.baseline_vals[self.lmarker]-self.baseline_vals[self.lmarker-1]) <= self.step_limit and abs(self.baseline_vals[self.lmarker-1]-self.baseline_vals[self.lmarker-2]) <= self.step_limit:
                            self.valid_value = self.baseline_vals[self.lmarker]
                            self.lmarker = self.lmarker + 1
                            for i in range(self.lmarker, self.jump_marker, 1):
                                self.baseline_vals[i] = self.valid_value

                            self.baseline_vals[self.jump_marker] = self.valid_value

                            self.lmarker = self.jump_marker
                            self.puffer_size = self.jump_marker + self.delay_size

                            on = 0
                            self.state_next = 2

                        else:
                            self.lmarker = self.lmarker-1

                else:
                    self.lmarker = self.lmarker + 1
                    self.baseline_vals[self.lmarker] = self.current_baseline_val

                    self.state_next = 1
            
            #-------------------------------------------------------------
            # state 2: identification of next self.valid_value after the blink
            #-------------------------------------------------------------
            
            if self.state_no == 2:
                # collecting values following the blink
                #- - - - - - - - - - - - - - - - - - - - - -
                if self.lmarker < self.puffer_size:
                    self.lmarker = self.lmarker + 1
                    self.baseline_vals[self.lmarker] = self.current_baseline_val

                    self.state_next = 2
            
                else:
                    # identification of next self.valid_value after the blink
                    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - 
                    if self.current_baseline_val > self.lower_th and abs(self.current_baseline_val-self.baseline_vals[self.lmarker]) <= self.step_limit and abs(self.baseline_vals[self.lmarker]-self.baseline_vals[self.lmarker-1]) <= self.step_limit:               
                        self.lmarker = self.lmarker + 1
                        self.baseline_vals[self.lmarker] = self.current_baseline_val

                        self.state_next = 1
                
                    else:
                        self.lmarker = self.lmarker + 1
                        self.baseline_vals[self.lmarker] = self.current_baseline_val
                        self.baseline_vals[self.lmarker-2] = self.valid_value

                        self.state_next = 2
            
            self.state_no = self.state_next
            
            # Draw the crosses
            baseline_cross_1 = visual.Line(self.win, start=(0, -20), end=(0, 20), lineColor=(-1, -1, -1))
            baseline_cross_2 = visual.Line(self.win, start=(-20, 0), end=(20, 0), lineColor=(-1, -1, -1))
            baseline_cross_1.draw()
            baseline_cross_2.draw()
            
            # check if all components have finished
            if not continueRoutine: break
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]): core.quit()
            
            # refresh the screen
            if continueRoutine: self.win.flip()
        # end while

        