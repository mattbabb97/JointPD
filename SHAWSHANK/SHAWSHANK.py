#  .-')    ('-. .-.   ('-.      (`\ .-') /` .-')    ('-. .-.   ('-.         .-') _ .-. .-')   
# ( OO ). ( OO )  /  ( OO ).-.   `.( OO ),'( OO ). ( OO )  /  ( OO ).-.    ( OO ) )\  ( OO )  
#(_)---\_),--. ,--.  / . --. /,--./  .--. (_)---\_),--. ,--.  / . --. /,--./ ,--,' ,--. ,--.  
#/    _ | |  | |  |  | \-.  \ |      |  | /    _ | |  | |  |  | \-.  \ |   \ |  |\ |  .'   /  
#\  :` `. |   .|  |.-'-'  |  ||  |   |  |,\  :` `. |   .|  |.-'-'  |  ||    \|  | )|      /,  
# '..`''.)|       | \| |_.'  ||  |.'.|  |_)'..`''.)|       | \| |_.'  ||  .     |/ |     ' _) 
#.-._)   \|  .-.  |  |  .-.  ||         | .-._)   \|  .-.  |  |  .-.  ||  |\    |  |  .   \   
#\       /|  | |  |  |  | |  ||   ,'.   | \       /|  | |  |  |  | |  ||  | \   |  |  |\   \  
# `-----' `--' `--'  `--' `--''--'   '--'  `-----' `--' `--'  `--' `--'`--'  `--'  `--' '--'  
#Joint Bar Pull: for use with subject + conspecific

"""original code by MHB"""
# Do NOT use without permission from author!!! Copyright pending.
                                                                
'''WRITTEN IN PYTHON 3.6'''

'''HOW TO USE THIS FILE'''

'''MASTER TODO LIST'''

'''FINISHED TODO ITEMS'''
#scrSize = (1024, 768)

import sys
import random               # Import the 'random' library which gives cool functions for randomizing numbers
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions

pygame.init()               # This initializes all pygame modules

# Grab the monkey name from monkey_names.txt
# Split the two monkey names by ' '
with open("monkey_names.txt") as f:
    monkey = f.read()
    monkey = monkey.split(' ')
# Grab the monkey group name from monkey_group.txt
with open("monkey_group.txt") as f:
    monkey_group = f.read()

# Set Current Date
today = time.strftime('%Y-%m-%d')

fps = 60

sys.path.append('c:/')
sys.path.append('..')
#from lrc1024 import *
from Matts_Dual_Toolbox import *

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("Incorrect.wav")           # This sets your incorrect sound

pelletPath = ['c:/pellet1.exe', 'c:/pellet2.exe']


def pellet(side = [0,1], num = 1):
    """Dispense [num] pellets - 2nd argument will change number of pellets when called. Prints 'Pellet' if `pellet.exe` is not found (for
       development). Waits 500ms between pellets."""
    """side = 0 for Left; side = 1 for Right"""
    for i in range(num):
        if os.path.isfile(pelletPath[side]):
            os.system(pelletPath[side])
        else:
            print ("Pellet for " + str(monkey[side]))
            
        pygame.time.delay(500)

#trial_number = 0
#def increment():
#        global trial_number
#        trial_number = trial_number + 1

def makeFileName(task = 'Task', format = 'csv'):
    """Return string of the form SubjectStooge_Task_Date.format."""
    return monkey[0] + '_' + monkey[1] + '_' + task + '_' + today + '.' + format


start_button = Box((200, 100), (512, 384), Color('gray'))
font = pygame.font.SysFont('Calibri', 20)
starttext = font.render('GO', 1, Color('black'))
startpos = starttext.get_rect(centerx = 512, centery = 384)


"""ICON CLASS -------------------------------------------------------------------------------------------------------"""


class Image(Box):
    '''Image sprite. Inherits from toolbox Box class. Loads image from `index` 
       (column, row) in spritesheet. Image is scaled to 200x200px and centered 
       at (400, 300).'''
    def __init__(self, PNG, position, scale):                                  # Pass the image and position (x,y)
        super(Image, self).__init__()
        image = pygame.image.load(PNG).convert_alpha()                          # image = image you passed in arguments
        self.size = image.get_size()                                            # Get the size of the image
        self.image = pygame.transform.smoothscale(image, scale)                 # Scale the image = scale inputted
        self.rect = self.image.get_rect()                                       # Get rectangle around the image
        self.rect.center = self.position = position                             # Set rectangle and center at position
        self.mask = pygame.mask.from_surface(self.image)                        # Creates a mask object

    def mv2pos(self, pos):
        """Move image to position (x, y)."""
        self.rect = self.image.get_rect()
        self.rect.center = self.pos = pos

"""TRIAL CLASS -----------------------------------------------------------------------------------------------------"""

class Trial(object):
    def __init__(self):
        '''Initialise trial with properties set to 0 or empty. `present` is True 
           when sample is presented, False when choice occurs.'''
        self.trial_number = 0
        self.trial_within_block = -1
        self.block = 1
        self.block_length = trials_per_block
        self.blocks_per_session = blocks_per_session
        self.LorR = (0, 0)
        self.startphase = True
        self.phase1_1 = False
        self.phase1_2 = False
        self.phase2 = False

        self.zone_touched = False
        
        self.stimID = 0
        self.stimuli = []
        self.trial_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1]        
        
        

    def new(self):
        global subselection
        global SELECT1
        self.trial_number += 1                                                # Increment trial number by 1
        self.trial_within_block += 1                                          # Increment trial within block by 1
        sound_chime.play()
        print("Trial: " + str(self.trial_number))
        print("Trial_within_block: " + str(self.trial_within_block))
        print(self.trial_type)

        if self.trial_within_block == self.block_length:                      # If this is the last trial in the block
            self.trial_within_block = 0                                       # Reset this to 0           
            self.newBlock()                                                   # Run .newBlock()
            print("Block Complete!")

        self.startphase = True
        self.phase1_1 = False
        self.phase1_2 = False
        self.phase2 = False
        self.start_time = 0
        self.response_order = "X"
        self.left_choice = "X"
        self.right_choice = "X"
        self.left_pellets = 0
        self.right_pellets = 0

        

        self.zone_touched = False

        self.create_stimuli()
        cursor1.mv2pos((275, 375))
        cursor2.mv2pos((725, 375))

    def newBlock(self):
        """Moves program to the next block and randomizes the trial types"""
        self.stimID = 0
        self.block += 1
        pseudorandomize(self.trial_type)

        if self.block > self.blocks_per_session:
            print("Session Complete!")
            pygame.quit()
            sys.exit()

    def create_stimuli(self):
        """Create the stimuli based on the trial type"""
        global icon_condition

        Images = [Image("square.png", (512, 400), (240, 240)),
                  Image("square.png", (512, 400), (240, 240)),
                  Image("triangle.png", (512, 400), (240, 240)),
                  Image("square.png", (512, 400), (240, 240)),
                  Image("triangle.png", (512, 400), (240, 240)),
                    Image("pull_zone.png", (-500, -500), (1000, 500)),
                    Image("pull_zone_cursor1.png", (-500, -500), (1000, 500)),
                    Image("pull_zone_cursor2.png", (-500, -500), (1000, 500))]

        self.stimuli = [Images[0], Images[1], Images[2], Images[3], Images[4]]

    def draw_icons(self):
        """Draw the start button at center of the screen"""
        self.stimuli[1].mv2pos((275, 650))
        self.stimuli[1].draw(bg)
        self.stimuli[2].mv2pos((275, 100))
        self.stimuli[2].draw(bg)
        self.stimuli[3].mv2pos((725, 650))
        self.stimuli[3].draw(bg)
        self.stimuli[4].mv2pos((725, 100))
        self.stimuli[4].draw(bg)

    def draw_pull_zone(self):
        """Draw the stimuli at their positions after start button is selected"""
        self.stimuli[1].mv2pos((512, -125))
        self.stimuli[1].draw(bg)
        self.stimuli[2].mv2pos((-500, -500))
        self.stimuli[2].size = 0
        self.stimuli[3].mv2pos((-500, -500))
        self.stimuli[3].size = 0

    def update_pull_zone(self, cursor):
        if cursor == 1:
            self.stimuli[2].mv2pos((512, -125))
            self.stimuli[2].size = (1000, 500)
            self.stimuli[2].draw(bg)
        elif cursor == 2:
            self.stimuli[3].mv2pos((512, -125))
            self.stimuli[3].size = (1000, 500)
            self.stimuli[3].draw(bg)

    def trial_duration(self):
        global duration
        global timer
        global SELECT1
        global SELECT2
        seconds = 0

        if seconds < duration:
            seconds = ((pygame.time.get_ticks() / 1000) - self.start_time - 1.000)
            #print(seconds)

        if seconds > duration and self.zone_touched == True:
            seconds = seconds
        elif seconds > duration and self.zone_touched == False:
            sound(False)
            print("No response made! WRONG!")
            self.write(data_file, 0)
            bg.fill(white)
            refresh(screen)
            pygame.time.delay(ITI*1000)
            self.startphase = True
            self.phase1_1 = False
            self.phase1_2 = False
            self.phase2 = False
            seconds = 0
            self.new()

        return seconds


    def response_time(self):
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() / 1000) - self.start_time - 1.000)

        return seconds

    def resetSample(self):
        '''Reset sample to left or right position.'''
        self.stimuli[0].mv2pos(pos[0])


# Start Phase ----------------------------------------------------------------------------------------
    def start(self):
        """Draw start_button, show response screen upon collision."""
        self.start_time = (pygame.time.get_ticks() / 1000)
        moveCursor(cursor1, side = 0, only = 'down, up')
        moveCursor(cursor2, side = 1, only = 'down, up')
        self.draw_icons()
        cursor1.draw(bg)
        cursor2.draw(bg)

        # Left Cursor 1 collides with Blue Square
        if cursor1.collides_with(self.stimuli[1]):
                print(1)
                self.selection1 = 1
                cursor1.mv2pos((350, 450))
                self.startphase = False
                self.phase1_1 = True
                
        # Left Cursor 1 collides with Yellow Triangle      
        if cursor1.collides_with(self.stimuli[2]):
                print(2)
                self.selection1 = 2
                cursor1.mv2pos((350, 450))
                self.startphase = False
                self.phase1_1 = True
                
        # Right Cursor 2 collides with Blue Square 
        if cursor2.collides_with(self.stimuli[3]):
                print(3)
                self.selection2 = 3
                cursor2.mv2pos((674, 450))
                self.startphase = False
                self.phase1_2 = True
        
        # Right Cursor 2 collides with Yellow Triangle 
        if cursor2.collides_with(self.stimuli[4]):
                print(4)
                self.selection2 = 4
                cursor2.mv2pos((674, 450))
                self.startphase = False
                self.phase1_2 = True
        
# Phase 1_1 ---------------------------------------------------------------------------------------------
    def draw_left_selection(self, selection):
        if selection == 1:
            self.stimuli[1].mv2pos((275, 375))
            self.stimuli[1].draw(bg)
        elif selection == 2:
            self.stimuli[2].mv2pos((275, 375))
            self.stimuli[2].draw(bg)

    def right_icons(self):
        self.stimuli[3].mv2pos((725, 650))
        self.stimuli[3].draw(bg)
        self.stimuli[4].mv2pos((725, 100))
        self.stimuli[4].draw(bg)
        self.draw_left_selection(self.selection1)
        cursor2.draw(bg)
        moveCursor(cursor2, side = 1, only = 'down, up')
        self.response_order = "L"

        if cursor2.collides_with(self.stimuli[3]):
                print(3)
                self.selection2 = 3
                cursor2.mv2pos((674, 450))
                self.phase1_1 = False
                self.phase2 = True

        if cursor2.collides_with(self.stimuli[4]):
                print(4)
                self.selection2 = 4
                cursor2.mv2pos((674, 450))
                self.phase1_1 = False
                self.phase2 = True 


# Phase 1_2 ---------------------------------------------------------------------------------------------
    def draw_right_selection(self, selection):
        if selection == 3:
            self.stimuli[3].mv2pos((725, 375))
            self.stimuli[3].draw(bg)
        elif selection == 4:
            self.stimuli[4].mv2pos((725, 375))
            self.stimuli[4].draw(bg)

    def left_icons(self):
        self.stimuli[1].mv2pos((275, 650))
        self.stimuli[1].draw(bg)
        self.stimuli[2].mv2pos((275, 100))
        self.stimuli[2].draw(bg)
        self.draw_right_selection(self.selection2)
        cursor1.draw(bg)
        moveCursor(cursor1, side = 0, only = 'down, up')
        self.response_order = "R"

        if cursor1.collides_with(self.stimuli[1]):
                print(1)
                self.selection1 = 1
                cursor2.mv2pos((674, 450))
                self.phase1_2 = False
                self.phase2 = True

        if cursor1.collides_with(self.stimuli[2]):
                print(2)
                self.selection1 = 2
                cursor2.mv2pos((674, 450))
                self.phase1_2 = False
                self.phase2 = True

# Phase 2 -------------------------------------------------------------------------------------------------------------

    def draw_both_selections(self):
        bg.fill(white)
        left_selection = self.selection1
        right_selection = self.selection2

        # Odds = square.png
        # Evens = triangle.png
        
        # Both Cooperate
        if left_selection == 1 and right_selection == 3:
            self.left_choice = "Coop"
            self.right_choice = "Coop"
            self.left_pellets = 3
            self.right_pellets = 3
            self.stimuli[1].mv2pos((275, 375))
            self.stimuli[1].draw(bg)
            self.stimuli[3].mv2pos((725, 375))
            self.stimuli[3].draw(bg)
            self.delay_duration()
            
        # Left Cooperate Right Defect
        elif left_selection == 1 and right_selection == 4:
            print("Left Cooperate, Right Defect")
            self.left_choice = "Coop"
            self.right_choice = "Defect"
            self.left_pellets = 0
            self.right_pellets = 4
            self.stimuli[1].mv2pos((275, 375))
            self.stimuli[1].draw(bg)
            self.stimuli[4].mv2pos((725, 375))
            self.stimuli[4].draw(bg)
            self.delay_duration()
            
        # Both Defect
        elif left_selection == 2 and right_selection == 4:
            print("Left Defect, Right Defect")
            self.left_choice = "Defect"
            self.right_choice = "Defect"
            self.left_pellets = 1
            self.right_pellets = 1
            self.stimuli[2].mv2pos((275, 375))
            self.stimuli[2].draw(bg)
            self.stimuli[4].mv2pos((725, 375))
            self.stimuli[4].draw(bg)
            self.delay_duration()            
            
        # Left Defect Right Cooperate
        elif left_selection == 2 and right_selection == 3:
            print("Left Defect, Right Cooperate")
            self.left_choice = "Defect"
            self.right_choice = "Coop"
            self.left_pellets = 4
            self.right_pellets = 0
            self.stimuli[2].mv2pos((275, 375))
            self.stimuli[2].draw(bg)
            self.stimuli[3].mv2pos((725, 375))
            self.stimuli[3].draw(bg)
            self.delay_duration()
        
# Phase 3 ---------------------------------------------------------------------------------------
    def run_delay_phase(self):
        self.payout_matrix(self.left_pellets, self.right_pellets)
        self.write(data_file)
        bg.fill(white)
        refresh(screen)
        pygame.time.delay(ITI * 1000)
        self.new()
        #self.stimuli[0].mv2pos((-50, -50))
        #self.stimuli[0].size = 0
        #cursor1.draw(bg)
        #cursor2.draw(bg)
        #self.delay_duration()

    def payout_matrix(self, left, right):
        if left == 3 and right == 3:
            pellet(side = 0, num = 3)
            pellet(side = 1, num = 3)
            self.delay_duration()
        elif left == 1 and right == 1:
            pellet(side = 0, num = 1)
            pellet(side = 1, num = 1)
            self.delay_duration()
        elif left == 0 and right == 4:
            pellet(side = 0, num = 0)
            pellet(side = 1, num = 4)
            self.delay_duration()
        elif left == 4 and right == 0:
            pellet(side = 0, num = 4)
            pellet(side = 1, num = 0)
            self.delay_duration()
            
    
    def delay_duration(self):
        global timer
        global SELECT1
        global SELECT2
        seconds = 0
        if seconds < 2:
            seconds = ((pygame.time.get_ticks() / 1000) - self.start_time)
            #print(seconds)

        if seconds > 2:
            self.phase1_1 = False
            self.phase1_2 = False
            self.phase2 = False
            self.phase3 = True
            print("Phase 3: True")
            seconds = 0

        return seconds
        

# Phase 2 -------------------------------------------------------------------------------------------
    def run_trial(self):
        global SELECT1
        global SELECT2
        global button_positions

        moveCursor(cursor1, side = 0, only = 'up, down')
        moveCursor(cursor2, side = 1, only = 'up, down')
        cursor1.draw(bg)
        cursor2.draw(bg)
        # Remove start button
        self.stimuli[0].mv2pos((-500, -500))
        self.stimuli[0].size = 0
        
        self.draw_pull_zone()
        self.trial_duration()
        self.response_time()

        self.zone_touched = False

        # If left cursor collides with the pull_zone, activate it to stimuli[2]
        if cursor1.collides_with(self.stimuli[1]):
            self.stimuli[1].mv2pos((-500, -500))                                    # Remove pull zone from the screen
            self.stimuli[1].size = 0
            self.update_pull_zone(cursor = 1)                                       # Draw cursor1's activated pull zone
            cursor1.draw(bg)                                                        # Draw cursor1 on top of the activated pull zone so it doesn't disappear
            cursor2.draw(bg)
            self.zone_touched = True
        # If right cursor collides with the pull_zone, activate it to stimuli[3]
        elif cursor2.collides_with(self.stimuli[1]):
            self.stimuli[1].mv2pos((-500, -500))                                      # Remove pull zone from the screen
            self.stimuli[1].size = 0
            self.update_pull_zone(cursor = 2)                                       # Draw cursor2's activated pull zone
            cursor2.draw(bg)                                                        # Draw cursor2 on top of the activated pull zone so it doesn't disappear
            cursor1.draw(bg)
            self.zone_touched = True

        # If neither cursor are colliding with the pull zone, remove the other pull zones from the screen
        elif SELECT1 == -1 and SELECT2 == -1:
            self.stimuli[2].mv2pos((-500, -100))
            self.stimuli[2].size = 0
            self.stimuli[3].mv2pos((-500, -100))
            self.stimuli[3].size = 0
            self.zone_touched = False

        if cursor1.collides_with(self.stimuli[3]) or cursor2.collides_with(self.stimuli[2]):
            sound(True)
            self.write(data_file, 1)
            #pellet(side = 0, num = 1)
            #pellet(side = 1, num = 1)
            bg.fill(white)
            refresh(screen)
            pygame.time.delay(ITI * 1000)
            self.new()


        # If the cursor is in the pull zone and its not moving, reset it to the start
            # This ensures monkey 1 is holding down the lever
        if cursor1.position[1] <= 125 and moveCursor(cursor1, side = 0) == False:
            cursor1.mv2pos((350, 450))
            # This ensures monkey 2 is holding down the lever
        if cursor2.position[1] <= 125 and moveCursor(cursor2, side = 1) == False:
            cursor2.mv2pos((674, 450))


    def left_or_right(self):
        global button_positions
        if self.LorR == 1:
            return "left"
        elif self.LorR == 2:
            return "right"

    def write(self, file):
        now = time.strftime('%H:%M:%S')
        session_type = "joint"
        time_taken = self.response_time()
        data = [monkey[0], monkey[1], today, now, self.block, self.trial_number, self.trial_type[self.trial_within_block], self.response_order,
                self.left_choice, self.right_choice, self.left_pellets, self.right_pellets]

        
        writeLn(file, data)
        


# SETUP
# get parameters
varNames = ['full_screen', 'trials_per_block', 'blocks_per_session', 'ITI', 'duration', 'run_time', 'time_out']
params = getParams(varNames)
globals().update(params)

full_screen = params['full_screen']
trials_per_block = params['trials_per_block']
blocks_per_session = params['blocks_per_session']
ITI = params['ITI']
duration = params['duration']
run_time = params['run_time']
time_out = params['time_out']

# set screen; define cursor; make left/right, top/bottom positions
screen = setScreen(full_screen)
pygame.display.set_caption('PRISON BREAK!!')
display_icon = pygame.image.load("Monkey_Icon.png")
pygame.display.set_icon(display_icon)
cursor1 = Box(circle = True, speed = 5)
cursor2 = Box(circle = True, speed = 5)
pos = [(150, 100), (874, 100), (150, 668), (874, 668)]

# create list of delays for a block (for pseudo-randomisation)
#delayList = delay * reps

# load file list
files = glob.glob('stimuli/*.png')

# start clock; stop program after [run_time] min x 60 seconds x 1000 ms
clock = pygame.time.Clock()
button_positions = [(120, 550), (920, 550)]

# save parameters and make data file with header

data_file = makeFileName('Simon_Says_Test')
writeLn(data_file, ['monkey_left', 'monkey_right', 'date', 'time', 'block', 'trial_number', 'trial_type',
                    'response_order', 'left_choice', 'right_choice', 'left_pellets', 'right_pellets', 'left_rt', 'right_rt'])



# MAIN GAME LOOP: start first trial
trial = Trial()
trial.new()



while True:
    quitEscQ(data_file)  # quit on [Q] or [Esc]
    timer = (pygame.time.get_ticks() / 1000)
    SELECT1 = cursor1.collides_with_list(trial.stimuli)
    #print("SELECT 1: " + str(SELECT1))
    SELECT2 = cursor2.collides_with_list(trial.stimuli)
    #print("SELECT 2: " + str(SELECT2))

    #for testing have it quit after 200 trials
    #current_time = pygame.time.get_ticks()

    if trial.trial_number > 200:
        pygame.quit()
        sys.exit()

    bg.fill(white)  # clear screen
    clock.tick(fps)
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1_1== True:
            trial.right_icons()
        elif trial.phase1_2 == True:
            trial.left_icons()
        elif trial.phase2 == True:
            trial.draw_both_selections()
        elif trial.phase3 == True:
            trial.run_delay_phase()
        else:
            pygame.quit()
            
            
    #if trial.startphase:
    #    trial.start()
    #elif trial.phase1:
    #    trial.sample() # else, if sample is to be presented, run sample subroutine
    #else:
    #    trial.matching()  # else, run matching subroutine

    refresh(screen)
    #clock.tick(fps)  # caps frame rate
