# This file has the Default Beat classes and subclasses

from AudioClass import *

class DefaultBeat(object):
    def __init__(self, soundboard):
        self.soundboard = soundboard
        self.kick = None
        self.snare = None
        self.openhihat = None
        self.closedhihat = None
        self.shaker = None
        self.kickTimes = set()
        self.snareTimes = set()
        self.openhihatTimes = set()
        self.closedhihatTimes = set()
        self.shakerTimes = set()
        self.timer = 150

    def getKick(self):
        freq = 440
        kick = self.soundboard.soundFiles[0][0]
        for row in range(self.soundboard.rows):
            for col in range(self.soundboard.cols):
                filename = self.soundboard.soundFiles[row][col]
                if (filename != []):    
                    f = Audio.getFrequency(filename)               
                    if f < freq and f > 3:
                        kick = filename
                        freq = f
        self.kick = kick

    def getSnare(self):
        snare = self.soundboard.soundFiles[0][0]
        for row in range(self.soundboard.rows):
            for col in range(self.soundboard.cols):
                filename = self.soundboard.soundFiles[row][col]
                if (filename != []):
                    if Audio.getFrequency(filename) > 75 and Audio.getFrequency(filename) < 200:
                        self.snare = filename
                        return
        self.snare = snare

    def getOpenHiHat(self):
        openhihat = self.soundboard.soundFiles[0][0]
        for row in range(self.soundboard.rows):
            for col in range(self.soundboard.cols):
                filename = self.soundboard.soundFiles[row][col]
                if (filename != []):
                    if Audio.getFrequency(filename) > 400 and Audio.getFrequency(filename) < 800:
                        self.openhihat = filename
                        return
        self.openhihat = openhihat

    def getClosedHiHat(self):
        closedhihat = self.soundboard.soundFiles[0][0]
        for row in range(self.soundboard.rows):
            for col in range(self.soundboard.cols):
                filename = self.soundboard.soundFiles[row][col]
                if (filename != []):
                    f = Audio.getFrequency(filename)
                    if f ==0 or f>1200:
                        self.closedhihat = filename
                        return
        self.closedhihat = closedhihat
        

# beat "Simple kick drum and claps beat" from library Trickshot soundsnap.com
class DefaultBeat1(DefaultBeat):
    def __init__(self, soundboard):
        super().__init__(soundboard)
        self.timer = 130
        self.kickTimes = set([0, 2, 10, 12, 16, 18, 26, 28])
        self.snareTimes = set([6,14,22,30])

# beat "Bassy hip hop beat with claps" from library Trickshot soundsnap.com
class DefaultBeat2(DefaultBeat):
    def __init__(self, soundboard):
        super().__init__(soundboard)
        self.timer = 110
        self.kickTimes = set([0, 2, 8, 16, 18, 24])
        self.snareTimes = set([6,14, 22, 30])
        self.closedhihatTimes = set([1, 4, 11, 12, 15, 17, 20, 27, 28, 31])


# beat from https://www.youtube.com/watch?v=FGNO_9Yqk_E
class DefaultBeat3(DefaultBeat):
    def __init__(self, soundboard):
        super().__init__(soundboard)
        self.timer = 140
        #self.kickTimes = set([1,6,8,11,14,15,17,22,24,27,30,31])
        #self.snareTimes = set([5,13,21,29,0])
        #self.closedhihatTimes = set([(2*i+1) for i in range(15)])
        self.kickTimes = set([0, 2, 10, 12, 16, 18, 26, 29])
        self.snareTimes = set([6,14, 22, 30])
        self.closedhihatTimes = set([(2*i+1) for i in range(0,15,2)])

# beat from Desiigner - Panda - https://www.youtube.com/watch?v=X_iAw_0-WRo
class DefaultBeat4(DefaultBeat):
    def __init__(self, soundboard):
        super().__init__(soundboard)
        self.timer = 85
        self.kickTimes = set([0, 15, 21,31])
        self.snareTimes = set([9,19, 25])
        self.closedhihatTimes = set([(2*i+1) for i in range(15)])
        self.openhihatTimes = set([13,29])

