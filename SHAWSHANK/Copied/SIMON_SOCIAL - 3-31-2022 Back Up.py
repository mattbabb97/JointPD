#  .-')            _   .-')                     .-') _         .-')                                      ('-.               
# ( OO ).         ( '.( OO )_                  ( OO ) )       ( OO ).                                   ( OO ).-.           
#(_)---\_)  ,-.-') ,--.   ,--.).-'),-----. ,--./ ,--,'       (_)---\_) .-'),-----.    .-----.  ,-.-')   / . --. / ,--.      
#/    _ |   |  |OO)|   `.'   |( OO'  .-.  '|   \ |  |\       /    _ | ( OO'  .-.  '  '  .--./  |  |OO)  | \-.  \  |  |.-')  
#\  :` `.   |  |  \|         |/   |  | |  ||    \|  | )      \  :` `. /   |  | |  |  |  |('-.  |  |  \.-'-'  |  | |  | OO ) 
# '..`''.)  |  |(_/|  |'.'|  |\_) |  |\|  ||  .     |/        '..`''.)\_) |  |\|  | /_) |OO  ) |  |(_/ \| |_.'  | |  |`-' | 
#.-._)   \ ,|  |_.'|  |   |  |  \ |  | |  ||  |\    |        .-._)   \  \ |  | |  | ||  |`-'| ,|  |_.'  |  .-.  |(|  '---.' 
#\       /(_|  |   |  |   |  |   `'  '-'  '|  | \   |        \       /   `'  '-'  '(_'  '--'\(_|  |     |  | |  | |      |  
# `-----'   `--'   `--'   `--'     `-----' `--'  `--'         `-----'      `-----'    `-----'  `--'     `--' `--' `------'  

#SOCIAL VERSION: for use with subject + conspecific

"""original code by JW, modified by MHB for project"""
                                                                
'''WRITTEN IN PYTHON 3.6'''

'''HOW TO USE THIS FILE'''
'''Edit stimuli images in stimuli folder'''
'''Change delays in the parameters txt file'''
'''Change subject/stooge in monkey names.txt'''

'''MASTER TODO LIST'''
# TODO-master: figure out how to do the delay

'''FINISHED TODO ITEMS'''
# Size of the Screen: scrSize = (1024, 768)
# TODO: 

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

pelletPath = ['c:/pellet.exe', 'c:/pellet2.exe']


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
        self.phase1 = False
        self.phase2 = False
        self.stimID = 0
        self.stimuli = []
        self.trial_type = [2, 1, 4, 3, 1, 4, 2, 3, 2, 3,
                           2, 1, 1, 3, 2, 4, 1, 4, 3, 4]
        pseudorandomize(self.trial_type)
        
        
        self.first_monkey = 0
        

    def new(self):
        global subselection
        global SELECT1
        #SELECT1 = -1
        self.trial_number += 1                                                # Increment trial number by 1
        self.trial_within_block += 1                                          # Increment trial within block by 1
        sound_chime.play()
        print("Trial: " + str(self.trial_number))
        print("Trial_within_block: " + str(self.trial_within_block))
        print(self.trial_type)
        #print("Block: " + str(self.block))

        if self.trial_within_block == self.block_length:                      # If this is the last trial in the block
            self.trial_within_block = 0                                       # Reset this to 0           
            self.newBlock()                                                   # Run .newBlock()
            print("Block Complete!")

        self.startphase = True
        self.phase1 = False
        self.phase2 = False
        self.seconds = 0

        self.create_stimuli()
        cursor1.mv2pos((450, 700))
        cursor2.mv2pos((574, 700))

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

        Images = [Image("start.png", (150, 200), (140, 140)),
                    Image("imageA.png", (0, 0), (150, 150)),
                    Image("imageB.png", (0, 0), (150, 150)),
                    Image("Blue_Button_Blank.png", (0, 0), (400, 400)),
                    Image("Red_Button_Blank.png", (0, 0), (400, 400)),
                    Image("blank_button.png", (0,0), (400, 400))]
        # Blue Triangle Trials
        if self.trial_type[self.trial_within_block] == 1 or self.trial_type[self.trial_within_block] == 3:
            self.stimuli = [Images[0], Images[1], Images[3], Images[4]]

        # Orange Circle Trials
        elif self.trial_type[self.trial_within_block] == 2 or self.trial_type[self.trial_within_block] == 4:
            self.stimuli = [Images[0], Images[2], Images[3], Images[4]]

        self.stimID += 1

    def draw_start(self):
        """Draw the start button at center of the screen"""
        self.stimuli[0].mv2pos((512, 500))
        self.stimuli[0].draw(bg)


    def draw_stimuli(self):
        """Draw the stimuli at their positions after start button is selected"""
        global button_positions

        if self.trial_type[self.trial_within_block] == 1:   # Blue Icon Right Congruent
            self.stimuli[1].mv2pos((920, 100))
            self.stimuli[1].draw(bg)
        elif self.trial_type[self.trial_within_block] == 3:   # Blue Icon Left Incongruent
            self.stimuli[1].mv2pos((104, 100))
            self.stimuli[1].draw(bg)
        elif self.trial_type[self.trial_within_block] == 2:   # Orange Icon Left Congruent
            self.stimuli[1].mv2pos((104, 100))
            self.stimuli[1].draw(bg)
        elif self.trial_type[self.trial_within_block] == 4:   # Orange Icon Right  Incongruent
            self.stimuli[1].mv2pos((920, 100))
            self.stimuli[1].draw(bg)

        self.stimuli[2].mv2pos(button_positions[1])
        self.stimuli[3].mv2pos(button_positions[0])
        self.stimuli[2].draw(bg)
        self.stimuli[3].draw(bg)

    def trial_duration(self):
        global duration
        global timer
        global SELECT1
        global SELECT2
        seconds = 0

        if seconds < duration:
            seconds = ((pygame.time.get_ticks() / 1000) - self.seconds)
            print(seconds)


        if seconds > duration and SELECT1 != -1:
            seconds = seconds
        elif seconds > duration and SELECT1 == -1:
            sound(False)
            self.write(data_file, 'NA', self.response_time(), 2)
            #self.trial_number -= 1
            #self.trial_within_block -= 1
            #self.stimID -= 1
            seconds = 0
            selection = 0
            self.startphase = True
            self.new()

        return seconds

    def response_time(self):
        seconds = 0
        if seconds < duration:
            seconds = ((pygame.time.get_ticks() / 1000) - self.seconds)

        return seconds

    def resetSample(self):
        '''Reset sample to left or right position.'''
        self.stimuli[0].mv2pos(pos[0])

    def start(self):
        """Draw start_button, show response screen upon collision."""
        self.seconds = (pygame.time.get_ticks() / 1000)
        moveCursor(cursor1, side = 0, only = 'up')
        moveCursor(cursor2, side = 1, only = 'up')
        self.draw_start()

        cursor1.draw(bg)
        cursor2.draw(bg)

        # If its a Purple Trial (Correct = Right), then only cursor2 can hit Start!
        if self.trial_type[self.trial_within_block] == 1 or self.trial_type[self.trial_within_block] == 3:
            if cursor2.collides_with(self.stimuli[0]):
                cursor1.mv2pos((450, 550))
                cursor2.mv2pos((574, 550))
                self.startphase = False
                self.phase1 = True
            elif cursor1.collides_with(self.stimuli[0]):
                cursor1.mv2pos((450, 700))

            
        # If its a Orange Trial (Correct = Left), then only cursor1 can hit Start!
        elif self.trial_type[self.trial_within_block] == 2 or self.trial_type[self.trial_within_block] == 4:
            if cursor1.collides_with(self.stimuli[0]):
                cursor1.mv2pos((450, 550))
                cursor2.mv2pos((574, 550))
                self.startphase = False
                self.phase1 = True
            elif cursor2.collides_with(self.stimuli[0]):
                cursor2.mv2pos((574, 700))


    def run_trial(self):
        global SELECT1
        global SELECT2
        global button_positions

        moveCursor(cursor1, side = 0, only = 'left, right')
        moveCursor(cursor2, side = 1, only = 'left, right')
        cursor1.draw(bg)
        cursor2.draw(bg)

        self.stimuli[0].mv2pos((-50, -50))
        self.stimuli[0].size = 0
        self.draw_stimuli()
        self.trial_duration()
        #self.response_time()


        # If the Blue Triangle Appears
        # Correct Button on the RIGHT SIDE
        if self.trial_type[self.trial_within_block] == 1 or self.trial_type[self.trial_within_block] == 3:
            
            if SELECT2 == 2:
                self.LorR = 2
                self.write(data_file, self.left_or_right(), self.response_time(), 1)
                sound(True)
                pellet(side = 0, num = 1)
                pellet(side = 1, num = 1)
                bg.fill(white)
                refresh(screen)
                pygame.time.delay(ITI * 1000)
                self.new()
            elif SELECT1 == 3:
                #self.LorR = button_positions[0]
                cursor1.mv2pos((450, 550))
                #self.write(data_file, self.response_time(), 0)
                #sound(False)
                #bg.fill(white)
                #refresh(screen)
                #pygame.time.delay(ITI * 1000)
                #self.new()
#                self.first_monkey = 1
                pass
                

        # If the Red Circle Appears
        # Correct Button on the LEFT SIDE
        elif self.trial_type[self.trial_within_block] == 2 or self.trial_type[self.trial_within_block] == 4:
            
            if SELECT2 == 2:
                #self.LorR = button_positions[1]
                cursor2.mv2pos((574, 550))
                #self.write(data_file, self.response_time(), 0)
                #sound(False)
                #bg.fill(white)
                #refresh(screen)
                #pygame.time.delay(ITI * 1000)
                #self.new()
                #self.first_monkey = 2
                
            elif SELECT1 == 3:
                self.LorR = 1
                self.write(data_file, self.left_or_right(), self.response_time(), 1)
                sound(True)
                pellet(side = 0, num = 1)
                pellet(side = 1, num = 1)
                bg.fill(white)
                refresh(screen)
                pygame.time.delay(ITI * 1000)
                self.new()

    def first_monkey(self):
        global button_positions
        if self.first_monkey == 1:
            return "left"
        elif self.first_monkey == 2:
            return "right"

    def left_or_right(self):
        global button_positions
        if self.LorR == 1:
            return "left"
        elif self.LorR == 2:
            return "right"

    def write(self, file, side, time_taken, correct):
        now = time.strftime('%H:%M:%S')
        session_type = "joint"
        if self.trial_type[self.trial_within_block] == 1 or self.trial_type[self.trial_within_block] == 3:
            self.icon_color = 1    # PURPLE
            data = [monkey[1], monkey[0], today, now, session_type, self.block, self.trial_number, self.trial_type[self.trial_within_block], side, time_taken,self.icon_color, correct]
        elif self.trial_type[self.trial_within_block] == 2 or self.trial_type[self.trial_within_block] == 4:
            self.icon_color = 2    # ORANGE
            data = [monkey[0], monkey[1], today, now, session_type, self.block, self.trial_number, self.trial_type[self.trial_within_block], side, time_taken,self.icon_color, correct]

        #data = [monkey[0], monkey[1], today, now, session_type, self.block, self.trial_number, self.trial_type[self.trial_within_block], side, time_taken,
        #       self.icon_color, correct]
        
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
pygame.display.set_caption('Simon Says Social')
display_icon = pygame.image.load("Monkey_Icon.png")
pygame.display.set_icon(display_icon)
cursor1 = Box(circle = True)
cursor2 = Box(circle = True, color = (black))
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
writeLn(data_file, ['monkey', 'stooge_monkey', 'date', 'time', 'session_type', 'block', 'trial_number', 'trial_type', 'response_side', 'response_time', 'blue_or_orange', 'correct_or_incorrect'])



# MAIN GAME LOOP: start first trial
trial = Trial()
trial.new()



while True:
    quitEscQ(data_file)  # quit on [Q] or [Esc]
    timer = (pygame.time.get_ticks() / 1000)
    SELECT1 = cursor1.collides_with_list(trial.stimuli)
    SELECT2 = cursor2.collides_with_list(trial.stimuli)
    #print(trial.seconds)

    #for testing have it quit after 200 trials
    #current_time = pygame.time.get_ticks()

    if trial.trial_number > 200:
        pygame.quit()
        sys.exit()

    bg.fill(Color('white'))  # clear screen
    clock.tick(fps)
    if trial.startphase == True:
        trial.start()
    elif trial.startphase == False:
        if trial.phase1 == True:
            trial.run_trial()
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
