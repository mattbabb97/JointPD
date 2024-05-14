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
# TODO:
# TODO: 

import sys
import random               # Import the 'random' library which gives cool functions for randomizing numbers
import math                 # Import the 'math' library for more advanced math operations
import time                 # Import the 'time' library for functions of keeping track of time (ITIs, IBIs etc.)
import datetime
import os                   # Import the operating system (OS)
import glob                 # Import the glob function
import pygame               # Import Pygame to have access to all those cool functions
#import Matts_Toolbox        # Import Matt's Toolbox with LRC specific functions

pygame.init()               # This initializes all pygame modules

# Grab the monkey name from monkey_names.txt
# Split the two monkey names by ' '
with open("monkey_names.txt") as f:
    monkey = f.read()
    monkey = monkey.split(' ')

# Set Current Date
today = time.strftime('%Y-%m-%d')

sys.path.append('c:/')
sys.path.append('..')
#from lrc1024 import *
from Matts_Dual_Toolbox import *

"""Put your sounds here"""
sound_chime = pygame.mixer.Sound("chime.wav")                   # This sets your trial initiation sound
sound_correct = pygame.mixer.Sound("correct.wav")               # This sets your correct pellet dispensing sound
sound_incorrect = pygame.mixer.Sound("Incorrect.wav")           # This sets your incorrect sound

#if os.path.exists('c:/'):
#    sndCor     = pygame.mixer.Sound('c:/correct.wav')
#    sndIncor   = pygame.mixer.Sound('c:/incorrect.wav')
#else:
#    sndCor = pygame.mixer.Sound('../correct.wav')
#    sndIncor = pygame.mixer.Sound('../incorrect.wav')

pelletPath = ['c:/pellet.exe', 'c:/pellet2.exe']



def pellet(side = [0,1], num = 1):
    """Dispense [num] pellets - 2nd argument will change number of pellets when called. Prints 'Pellet' if `pellet.exe` is not found (for
       development). Waits 500ms between pellets."""
    for i in range(num):
        if os.path.isfile(pelletPath[side]):
            os.system(pelletPath[side])
        else:   print ("Pellet for " + str(monkey[side]))
        pygame.time.delay(500)

trial_number = 0
def increment():
        global trial_number
        trial_number = trial_number + 1

def makeFileName(task = 'Task', format = 'csv'):
    """Return string of the form SubjectStooge_Task_Date.format."""
    return monkey[1] + monkey[0] + '_' + task + '_' + today + '.' + format


start_button = Box((200, 100), (512, 384), Color('gray'))
font = pygame.font.SysFont('Calibri', 20)
starttext = font.render('START', 1, Color('black'))
startpos = starttext.get_rect(centerx = 512, centery = 384)


# HELPER CLASSES
class Image(Box):
    '''Image sprite. Inherits from toolbox Box class. Loads image from `index` 
       (column, row) in spritesheet. Image is scaled to 200x200px and centered 
       at (400, 300).'''
    def __init__(self, index):
        super(Image, self).__init__()
        image = pygame.image.load(files[index]).convert_alpha()
        self.size = image.get_size()
        self.image = pygame.transform.smoothscale(image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos = (512, 384)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = files[index][8:-4]

    def mv2pos(self, pos):
        """Move image to position (x, y)."""
        self.rect = self.image.get_rect()
        self.rect.center = self.pos = pos

class Trial(object):
    def __init__(self):
        '''Initialise trial with properties set to 0 or empty. `present` is True 
           when sample is presented, False when choice occurs.'''
        self.number = 0
        self.subtrial = 0
        self.block = 0
        self.blockLen = len(delayList)
        self.present = True
        self.stimuli = []
        self.isStartScreen = True

    def new(self):
        '''Increment trial number and determine trial number within the block.
           At the end of a block, start a new one. Set `present` to True to 
           present sample. Make stimuli and reset cursor to screen center.'''
        self.number += 1
        self.subtrial = (self.number - 1) % self.blockLen
        if self.subtrial == 0:    self.newBlock()

        self.present = True
        trial.isStartScreen = True
        self.makeStimuli()
        increment()
        cursor.mv2pos((512, 618))
        cursor1.mv2pos((600, 400))

    def newBlock(self):
        '''Increment block counter, pseudo-randomise delays for next block, and 
           start inter-block interval.'''
        global timer

        self.block += 1
        random.shuffle(delayList)

        if self.number > 1:     timer = IBI * clock.get_fps()
        else:                   timer = 0

    def makeStimuli(self):
        """Pick four non-identical stimuli. Randomize left/right, top/bottom position."""
        idx = random.sample(range(len(files)), 4)
        self.stimuli = [Image(i) for i in idx]

        random.shuffle(pos)

        for i,s in enumerate(self.stimuli):
            s.mv2pos(pos[i])


    def drawSample(self):
        '''Draw sample in center of screen.'''
        self.stimuli[0].mv2pos((512, 384))
        self.stimuli[0].draw(bg)

    def resetSample(self):
        '''Reset sample to left or right position.'''
        self.stimuli[0].mv2pos(pos[0])

    def start(self):
        """Draw start_button, show response screen upon collision."""
        moveCursor(cursor, only='up', side = 0)
        moveCursor(cursor1, side = 1)

        start_button.draw(bg)
        bg.blit(starttext, startpos)
        cursor.draw(bg)
        cursor1.draw(bg)

        if cursor.collides_with(start_button):
            cursor.mv2pos((512, 384))
            self.isStartScreen = False

    def sample(self):
        '''Display sample: display blank screen for specified delay.'''
        # start_button.draw(bg)
        # mvCursor(cursor, only = 'up')
        # cursor.draw(bg)
        # if start == 0:
        self.present = False
        refresh(screen)
        if delayList[self.subtrial] == 5:
            bg.fill(Color('light sky blue'))
            refresh(screen)
            pygame.time.delay(2000)
            self.drawSample()
            refresh(screen)
            pygame.time.delay(2000)
            bg.fill(Color('light sky blue'))
        else:
            bg.fill(Color('white'))
            pygame.time.delay(2000)
            self.drawSample()
            refresh(screen)
            pygame.time.delay(2000)
            bg.fill(Color('white'))
        refresh(screen)
        self.resetSample()
        cursor.mv2pos((512, 384))
        '''for training'''
        #pygame.time.delay(delayList[self.subtrial] * 1000)
        '''for testing'''
        pygame.time.delay(1000)

    def matching(self):
        '''Display matches, upon selection: pellet + ITI (if correct) or timeout
           (if incorrect).'''
        if delayList[self.subtrial] == 5:
            bg.fill(Color('light sky blue'))
        else:
            bg.fill(Color('white'))

        for s in self.stimuli: s.draw(bg)

        moveCursor(cursor, side = 0)
        cursor.draw(bg)

        '''POTENTIAL PELLET OUTCOMES BASED ON PRESSURE CONDITION AND PERFORMANCE'''
        '''first pellet argument is side 0 = left, 1 = right'''
        if delayList[self.subtrial] == 5:
            if select > -1:
                if select == 0:
                    sound(True)
                    pellet(1,3)
                    bg.fill(Color('light sky blue'))
                    refresh(screen)
                    pygame.time.delay(ITI * 1000)
                    self.write(file, 'correct')
                    self.new()
                else:
                    sound(False)
                    pellet(0,3)
                    bg.fill(Color('light sky blue'))
                    refresh(screen)
                    pygame.time.delay(timeout * 1000)
                    self.write(file, 'incorrect')
                    self.new()
        else:
            if select > -1:
                if select == 0:
                    sound(True)
                    pellet(1)
                    bg.fill(Color('white'))
                    refresh(screen)
                    pygame.time.delay(ITI * 1000)
                    self.write(file, 'correct')
                    self.new()
                else:
                    sound(False)
                    bg.fill(Color('white'))
                    refresh(screen)
                    pygame.time.delay(timeout * 1000)
                    self.write(file, 'incorrect')
                    self.new()

    def write(self, file, response):
        '''Write data to file.'''
        now = time.strftime('%H:%M:%S')
        names = [s.name for s in self.stimuli]

        if pos[0] == (150, 100):    match_pos = 'top left'
        elif pos[0] == (874, 100):    match_pos = 'top right'
        elif pos[0] == (150, 668):    match_pos = 'bottom left'
        else:                         match_pos = 'bottom right'

        data = [monkey[1], monkey[0], today, now, self.number, self.block, delayList[self.subtrial], response] + names + [match_pos]
        writeLn(file, data)
        #print (data)



# SETUP
# get parameters
varNames = ['fullscreen', 'delay', 'reps', 'ITI', 'timeout', 'IBI', 'run_time']
params = getParams(varNames)
globals().update(params)

# set screen; define cursor; make left/right, top/bottom positions
screen = setScreen(fullscreen)
pygame.display.set_caption('Simon Says Social')
cursor = Box(circle = True)
cursor1 = Box(circle = True)
pos = [(150, 100), (874, 100), (150, 668), (874, 668)]

# create list of delays for a block (for pseudo-randomisation)
delayList = delay * reps

# load file list
files = glob.glob('stimuli/*.png')

# start clock; stop program after [run_time] min x 60 seconds x 1000 ms
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
stop_after = run_time * 60 * 1000

# save parameters and make data file with header

file = makeFileName('CapChoke')
writeLn(file, ['subject', 'stooge', 'date', 'time', 'trial', 'block', 'delay', 'response', 'match', 'foil1', 'foil2', 'foil3', 'match_pos'])


# MAIN GAME LOOP: start first trial
trial = Trial()
trial.new()

while True:
    quitEscQ(file)  # quit on [Q] or [Esc]

    # check and quit programme after certain overall run time
    '''current_time = pygame.time.get_ticks()
    if (current_time - start_time) > stop_after:
        pygame.quit()
        sys.exit()'''

    #for testing have it quit after 200 trials
    current_time = pygame.time.get_ticks()
    if trial_number > 200:
        pygame.quit()
        sys.exit()

    bg.fill(Color('white'))  # clear screen
    select = cursor.collides_with_list(trial.stimuli)  # check if cursor collides with anything

    if timer > 0:   timer -= 1  # if there is an inter-block interval, count down timer
    elif trial.isStartScreen: trial.start()
    elif trial.present:  trial.sample() # else, if sample is to be presented, run sample subroutine
    else:                trial.matching()  # else, run matching subroutine

    refresh(screen)
    clock.tick(fps)  # caps frame rate
