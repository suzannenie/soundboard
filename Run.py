# This file is the run page

# I use the cmu 112 animation framework and the modal app structure from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html and
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html


from cmu_112_graphics import *
from tkinter import *
import random, math, copy
import numpy as np
import pyaudio
import wave
import time
import threading
from AudioClass import *
from DefaultBeats import *
from Soundboards import *



class MyApp(ModalApp):
    def appStarted(app):
        app.startPage = StartPage()
        app.soundboardPage = SoundboardPage()
        app.automatePage = AutomatePage()
        app.effectsPage = EffectsPage()
        app.helpPage = HelpPage()
        app.setActiveMode(app.startPage)

app = MyApp(width = 500, height = 500)

# print(time.time())
# print('A', Audio.getFrequency('440Hz.wav'))


# print("bassdrum", Audio.getFrequency('bassdrum.wav'))
# print('bass2', Audio.getFrequency('bassdrum2.wav'))
# print('bass3', Audio.getFrequency('bassdrum3.wav'))
# print('drykick', Audio.getFrequency('drykick.wav'))
# print('floortom', Audio.getFrequency('floortom.wav'))
# print(Audio.trimAllSilence('snare.wav'))
# print("snare", Audio.getFrequency('snare.wav'))
# print("snare1", Audio.getFrequency('snare1.wav'))
# print("snare2", Audio.getFrequency('snare2.wav'))
# print("snare3", Audio.getFrequency('snare3.wav'))
# print("snare4", Audio.getFrequency('snare4.wav'))
# print("snare5", Audio.getFrequency('snare5.wav'))
# print("snare6", Audio.getFrequency('snare6.wav'))
# print("clap1", Audio.getFrequency('clap1.wav'))
# print("clap2", Audio.getFrequency('clap2.wav'))
# print("clap3", Audio.getFrequency('clap3.wav'))
# print('open', Audio.getFrequency('open.wav'))
# print('closed', Audio.getFrequency('closed.wav'))

# print("airplane", Audio.getFrequency('airplane.wav'))
# print("baboon", Audio.getFrequency('baboon.wav'))
# print("cardoor", Audio.getFrequency('cardoor.wav'))
# print("snaps", Audio.getFrequency('snaps.wav'))
# print("slurp", Audio.getFrequency('slurp.wav'))
# print("scream", Audio.getFrequency('scream.wav'))
# print('yell', Audio.getFrequency('yell.wav'))
# print('bark', Audio.getFrequency('bark.wav'))

# print('dodgers', Audio.getFrequency('dodgers.wav'))




