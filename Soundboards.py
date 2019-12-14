# This file contains the main soundboard classes and its subclasses

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


class Soundboard(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.keys = []
        self.soundFiles = []
        self.pressed = []

    def assignKeys(self):
        firstRow = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        secondRow = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
        thirdRow = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';']
        fourthRow = ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']

        allKeys = [firstRow, secondRow, thirdRow, fourthRow]
        
        for row in range (self.rows):
            rowKeys = []
            sounds = []
            press = []
            for col in range (self.cols):
                rowKeys.append(allKeys[row][col])
                sounds.append([])
                press.append(False)
            self.keys.append(rowKeys)
            self.soundFiles.append(sounds)
            self.pressed.append(press)
    
    def getRowandColfromFile(self, file):
        for row in range (self.rows):
            for col in range (self.cols):
                if file == self.soundFiles[row][col]:
                    return row, col


class StartPage(Mode):
    ROWS = 0
    COLS = 0

    def appStarted(mode):
        mode.rows = [1,2,3,4]
        mode.rowbolds = [1,1,1,1]
        boxSize = mode.width/12
        mode.rowDims = []

        for i in range(0, 8, 2):
            x1, x2 = mode.width/20 + boxSize*i, mode.width/10 + boxSize*(i+1)
            y1, y2 = mode.height/4, mode.height/4 + boxSize
            mode.rowDims.append((x1,y1,x2,y2))
        
        mode.selectedRow = 0
        mode.hasRowSelected = False

        mode.cols = [1,2,3,4,5,6,7,8,9,10]
        mode.colbolds = [1,1,1,1,1,1,1,1,1,1]
        mode.colDims = []

        for i in range(0, 10, 2):
            x1, x2 = mode.width/20 + boxSize*i, mode.width/10 + boxSize*(i+1)
            y1, y2 = mode.height/60*32, mode.height/60*32 + boxSize
            mode.colDims.append((x1,y1,x2,y2))
        for i in range(0, 10, 2):
            x1, x2 = mode.width/20 + boxSize*i, mode.width/10 + boxSize*(i+1)
            y1, y2 = mode.height/12*8, mode.height/12*8 + boxSize
            mode.colDims.append((x1,y1,x2,y2))
        
        mode.selectedCol = 0
        mode.hasColSelected = False
       

    def drawStartButton(mode, canvas):
        canvas.create_rectangle(mode.width*9/12, mode.height/20*17, 
                                mode.width*11/12, mode.height/20*18,
                                width = 3)
        canvas.create_text(mode.width*10/12, mode.height/40*35, 
                        text = "Start", font = f"Impact {14}")
    
    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2, mode.height/10, 
            text = "Create Your Soundboard", font = f"Impact {mode.width//18}")
        
        mode.drawStartButton(canvas)
       
        canvas.create_text(mode.width/10, mode.height/5, text = "Rows", 
            font = f"Impact {mode.width//24}")

        canvas.create_text(mode.width/10, mode.height/24*11, text = "Columns", 
            font = f"Impact {mode.width//24}")
        
        for i in range(4):
            x1, y1, x2, y2 = mode.rowDims[i]
            canvas.create_rectangle(x1, y1, x2, y2, width = mode.rowbolds[i])
            canvas.create_text((x2+x1)/2, (y2+y1)/2,text=f'{mode.rows[i]}')

        for i in range(10):
            x1, y1, x2, y2 = mode.colDims[i]
            canvas.create_rectangle(x1, y1, x2, y2, width= mode.colbolds[i])
            canvas.create_text((x2+x1)/2, (y2+y1)/2,text=f'{mode.cols[i]}')

    def mousePressed(mode, event):
        
        #select a row
        for i in range(4):
            x1, y1, x2, y2 = mode.rowDims[i]
            if event.x>x1 and event.x<x2 and event.y>y1 and event.y<y2:

                if mode.hasRowSelected and mode.selectedRow == i:
                    x1a, y1a, x2a, y2a = mode.rowDims[mode.selectedRow]
                    x1a -= mode.width/100
                    x2a += mode.width/100
                    y1a -= mode.height/100
                    y2a += mode.height/100
                    mode.rowDims[mode.selectedRow] = (x1a, y1a, x2a, y2a)
                    mode.rowbolds[mode.selectedRow] = 1
                    mode.hasRowSelected = False

                else:
                    x1 += mode.width/100
                    x2 -= mode.width/100
                    y1 += mode.height/100
                    y2 -= mode.height/100
                    mode.rowDims[i] = (x1, y1, x2, y2)
                    mode.rowbolds[i] = 3
                    if mode.hasRowSelected:
                        x1a, y1a, x2a, y2a = mode.rowDims[mode.selectedRow]
                        x1a -= mode.width/100
                        x2a += mode.width/100
                        y1a -= mode.height/100
                        y2a += mode.height/100
                        mode.rowDims[mode.selectedRow] = (x1a, y1a, x2a, y2a)
                        mode.rowbolds[mode.selectedRow] = 1
                    mode.hasRowSelected = True
                    mode.selectedRow = i

        #select a column
        for i in range(10):
            x1, y1, x2, y2 = mode.colDims[i]
            if event.x>x1 and event.x<x2 and event.y>y1 and event.y<y2:

                if mode.hasColSelected and mode.selectedCol == i:

                    x1a, y1a, x2a, y2a = mode.colDims[mode.selectedCol]
                    x1a -= mode.width/100
                    x2a += mode.width/100
                    y1a -= mode.height/100
                    y2a += mode.height/100
                    mode.colDims[mode.selectedCol] = (x1a, y1a, x2a, y2a)
                    mode.colbolds[mode.selectedCol] = 1
                    mode.hasColSelected = False

                else:
                    x1 += mode.width/100
                    x2 -= mode.width/100
                    y1 += mode.height/100
                    y2 -= mode.height/100
                    mode.colDims[i] = (x1, y1, x2, y2)
                    mode.colbolds[i] = 3
                    if mode.hasColSelected:
                        x1a, y1a, x2a, y2a = mode.colDims[mode.selectedCol]
                        x1a -= mode.width/100
                        x2a += mode.width/100
                        y1a -= mode.height/100
                        y2a += mode.height/100
                        mode.colDims[mode.selectedCol] = (x1a, y1a, x2a, y2a)
                        mode.colbolds[mode.selectedCol] = 1
                    mode.hasColSelected = True
                    mode.selectedCol= i

        # clicked start
        if mode.hasRowSelected and mode.hasColSelected:
            if event.x > mode.width*9/12 and event.y > mode.height/20*17 and \
                    event.x < mode.width*11/12 and event.y < mode.height/20*18:
                StartPage.ROWS = int(mode.selectedRow) + 1
                StartPage.COLS = int(mode.selectedCol) + 1

                mode.app.setActiveMode(mode.app.soundboardPage)


class SoundboardPage(Mode):
    def setRowsandCols(mode):
        mode.rows = StartPage.ROWS
        mode.cols = StartPage.COLS

    def appStarted(mode):
        mode.setRowsandCols()
        mode.soundboard = Soundboard(mode.rows, mode.cols)
        mode.margin = 20
        mode.topMargin = 30
        mode.squareWidth = (mode.width - 2*mode.margin) // mode.cols
        mode.squareHeight = (mode.height - 2*mode.margin - \
                            mode.topMargin) // mode.rows
        
        mode.soundboard.assignKeys() 
        mode.isRecording = False
        mode.isCreating = False
        mode.listtimes = []
        mode.listsounds = []
        mode.setSounds = set()
        mode.defaultbeatDict = dict()


    # adapted from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getSquareCoordinates(mode, row, col):
        x1 = mode.margin + col*mode.squareWidth + mode.width//50
        x2 = mode.margin + (col+1)*mode.squareWidth - mode.width//50
        y1 = mode.margin + mode.topMargin + \
            row * mode.squareHeight + mode.height//50
        y2 = mode.margin + mode.topMargin + \
            (row+1)*mode.squareHeight - mode.height//50
        return (x1, y1, x2, y2)
    
    def getRowandCol(mode, x, y):
        if x > mode.width - mode.margin - mode.width//50 \
            or x < mode.margin + mode.width//50 \
            or y > mode.height - mode.margin - mode.height//50 \
            or y < mode.margin + mode.topMargin + mode.height//50:
            return (-1, -1)
        row = int((y - mode.margin - mode.topMargin) / mode.squareHeight)
        col = int((x - mode.margin) / mode.squareWidth)
        return (row, col)

    def drawBoard(mode, canvas):
        canvas.create_rectangle(mode.margin, mode.margin+mode.topMargin, 
                    mode.width - mode.margin, mode.height-mode.margin, 
                    width = 3)
        
        for row in range (mode.rows):
            for col in range(mode.cols):
                x1, y1, x2, y2 = mode.getSquareCoordinates(row, col)
                w = 3

                if mode.soundboard.pressed[row][col]:
                    color = 'moccasin'
                    x1 += mode.width/120
                    x2 -= mode.width/120
                    y1 += mode.height/120
                    y2 -= mode.height/120
                    w = 4
                else:
                    color = "Light Yellow"

                canvas.create_rectangle(x1, y1, x2, y2, width = w, 
                                fill = color)
                canvas.create_text(mode.margin + (col+1/2)*mode.squareWidth,
                    mode.margin + (row+1/2)*mode.squareHeight + mode.topMargin,
                                text = mode.soundboard.keys[row][col])
                
                filename = mode.soundboard.soundFiles[row][col]
                canvas.create_text(mode.margin + (col+1/2)*mode.squareWidth,
                mode.margin + (row+1/2)* \
                    mode.squareHeight - mode.squareHeight//5 + mode.topMargin,
                        text = filename[:-4], font =f"Times {mode.width//50}")

    def drawRecordButton(mode, canvas):
        canvas.create_oval(mode.width*47/60, mode.margin -10, 
                                mode.width*57/60, mode.margin +20,
                                fill = "red", width = 3)
        if mode.isRecording:
            canvas.create_text(mode.width*52/60, mode.margin + 5, 
                        text = "Stop", font = f"Times {14} bold")
            canvas.create_rectangle(mode.width*19/60, mode.margin -10, 
                                mode.width*42/60, mode.margin +20,
                                fill = "white", width = 3)
            canvas.create_text(mode.width*6/12, mode.margin + 5, 
                        text = "**Recording**", font = f"Times {14} bold")
        else:
            canvas.create_text(mode.width*52/60, mode.margin + 2, 
                        text = "Voice", font = f"Times {12} bold")
            canvas.create_text(mode.width*52/60, mode.margin + 9, 
                        text = "Record", font = f"Times {12} bold")

    def drawCreateButton(mode, canvas):
        canvas.create_oval(mode.width*35/60, mode.margin -10, 
                                mode.width*45/60, mode.margin +20,
                                fill = "darkseagreen", width = 3)
        if mode.isCreating:
            canvas.create_text(mode.width*40/60, mode.margin + 5, 
                        text = "Stop", font = f"Times {14} bold")
            canvas.create_rectangle(mode.width*13/60, mode.margin -10, 
                                mode.width*33/60, mode.margin +20,
                                fill = "white", width = 3)
            canvas.create_text(mode.width*23/60, mode.margin + 5, 
                        text = "**Creating Beat**", font = f"Times {14} bold")
        else:
            canvas.create_text(mode.width*40/60, mode.margin + 5, 
                        text = "Create", font = f"Times {14} bold")

    def drawAutomateButton(mode, canvas):
        canvas.create_rectangle(mode.width*23/60, mode.margin -10, 
                                mode.width*33/60, mode.margin +20,
                                fill = "lightblue", width = 3)
        canvas.create_text(mode.width*28/60, mode.margin + 5, 
                        text = "Automate", font = f"Times {14} bold")

    def drawEffectsButton(mode, canvas):
        canvas.create_rectangle(mode.width*11/60, mode.margin -10, 
                                mode.width*21/60, mode.margin +20,
                                fill = "orchid", width = 3)
        canvas.create_text(mode.width*16/60, mode.margin + 5, 
                        text = "Effects", font = f"Times {14} bold")

    def drawHelpButton(mode, canvas):
        canvas.create_rectangle(mode.width*3/60, mode.margin -10, 
                                mode.width*9/60, mode.margin +20,
                                fill = "white", width = 3)
        canvas.create_text(mode.width*6/60, mode.margin + 5, 
                        text = "Help", font = f"Times {14} bold")

    def mousePressed(mode, event):
        row, col = mode.getRowandCol(event.x, event.y)

        # clicked outside of board
        if (row, col) == (-1, -1):
             # clicked record or stop button
            if event.x > mode.width*47/60 and event.x < mode.width*57/60 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:

                if mode.isRecording:
                    mode.isRecording = False
                else:
                    output = mode.getUserInput("Name your file: ")
                    if output == None:
                        return
                    output = output + ".wav"
                    # adapted from https://realpython.com/intro-to-python-threading/
                    y = threading.Thread(target=mode.voiceRecord, args = (output,), daemon = True)                    
                    y.start()

            if not mode.isRecording:
                # clicked create
                if event.x > mode.width*35/60 and event.x < mode.width*45/60 \
                    and event.y > mode.margin -10 and event.y < mode.margin +20:
                    if mode.isCreating:
                        mode.isCreating = False

                        if len(mode.listtimes) != 0:
                            mode.getCreatedBeat()
                            
                            
                    else:
                        mode.listtimes = []
                        mode.listsounds = []
                         
                        output = mode.getUserInput("Name your file: ")
                        if output == None:
                            return
                        output = output + ".wav"
                            
                        y = threading.Thread(target=mode.createFile, args = (output,), daemon = True)                    
                        y.start()     
                        mode.isCreating = True           

            if not mode.isRecording and not mode.isCreating:
                # clicked automate button
                if event.x > mode.width*23/60 and event.x < mode.width*33/60 \
                    and event.y > mode.margin -10 and event.y < mode.margin +20:
                    mode.app.setActiveMode(mode.app.automatePage)

                # clicked effects button
                elif event.x > mode.width*11/60 and event.x < mode.width*21/60 \
                    and event.y > mode.margin -10 and event.y < mode.margin +20:
                    mode.app.setActiveMode(mode.app.effectsPage)

                # clicked help button
                elif event.x > mode.width*3/60 and event.y > mode.margin -10 \
                    and event.x < mode.width*9/60 and event.y < mode.margin +20:
                    mode.app.setActiveMode(mode.app.helpPage)


        else:
            # clicked a square
            key = mode.soundboard.keys[row][col]
            path = \
            mode.getUserInput("Enter a .wav file to assign to key '" + key + "':")
            if path == None:
                return
            if (path != None):
                while not os.path.isfile(path):
                        path = mode.getUserInput\
                        ("Make sure the .wav file is in the same folder")
                        if (path == None):
                            return
                while (not path.endswith(".wav")):
                    path = mode.getUserInput\
                        ("Enter a .wav file \ to assign to key '" + key + "':")
                    if (path == None):
                        return
                    
            mode.soundboard.soundFiles[row][col] = path


    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    def playCallback(mode, path, row, col):

        wf = wave.open(path, 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        mode.soundboard.pressed[row][col] = True
        if mode.isCreating:
            mode.listtimes.append(time.time())
            mode.listsounds.append(mode.soundboard.soundFiles[row][col])

        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            if not mode.soundboard.pressed[row][col]:
                break
            time.sleep(0.1)

        # stop stream (6)
        stream.stop_stream()
        mode.soundboard.pressed[row][col] = False
        stream.close()
        wf.close()

        # close PyAudio (7)
        p.terminate()

    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    # and https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
    def playCallback2(mode, path, row, col):
        if len(sys.argv) < 2:
            print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
            #sys.exit(-1)

        wf = wave.open(path, 'rb')

        p = pyaudio.PyAudio()

        mode.soundboard.pressed[row][col] = True

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        stream.start_stream()

        data = wf.readframes(800)

        # int(RATE / CHUNK * RECORD_SECONDS)
        for i in range(0, int(44100 / 800 * 0.3)):
            if not mode.soundboard.pressed[row][col]:
                break
            stream.write(data)
            data = wf.readframes(800)

        stream.stop_stream()
        mode.soundboard.pressed[row][col] = False
        stream.close()
        wf.close()

        p.terminate()

    
    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    def voiceRecord(mode, filename):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')
        mode.isRecording = True

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        while mode.isRecording:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print('Finished recording')
        mode.isRecording = False

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def getCreatedBeat(mode):
        mode.defaultbeatDict = dict()
        mode.setSounds = set(mode.listsounds)
        startTime = mode.listtimes[0]

        for i in range(len(mode.listtimes)):
            # help from https://www.programiz.com/python-programming/methods/built-in/round
            mode.listtimes[i] = round(mode.listtimes[i] - startTime,2)

        for sound in mode.setSounds:
            mode.defaultbeatDict[sound] = set()
        
        for i in range(len(mode.listtimes)):
            mode.defaultbeatDict[mode.listsounds[i]].add(mode.listtimes[i])

    def playDefaultBeat(mode):
        thisTime = time.time()
        currTime = round(time.time()-thisTime,2)
        tempDict = mode.defaultbeatDict

        while currTime <= math.ceil(mode.listtimes[-1]):
            for sound in tempDict:
                if currTime in tempDict[sound]:

                    tempDict[sound].remove(currTime)
                    row, col = mode.soundboard.getRowandColfromFile(sound)
                    # adapted from https://realpython.com/intro-to-python-threading/
                    x = threading.Thread(target=mode.playCallback2, args = (sound,row, col), daemon = True)
                    x.start()
            currTime = round(time.time()-thisTime,2)

    def createFile(mode, filename):
        # adapted from https://realpython.com/intro-to-python-threading/
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Creating')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        while mode.isCreating:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print('Finished creating')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def appendSound(mode, soundbytes, frames):
        soundbytes = soundbytes
        oldFrames = frames
        return oldFrames + soundbytes
       

    def keyPressed(mode, event):
        for row in range (mode.rows):
            for col in range(mode.cols):
                
                #press space to stop playing
                if mode.soundboard.pressed[row][col]:
                    if event.key == "Space":
                        mode.soundboard.pressed[row][col] = False
                
                key = mode.soundboard.keys[row][col]                
                
                if (event.key == key):                 
                    filename = mode.soundboard.soundFiles[row][col]

                    if filename == []:
                        pass
                    elif os.path.isfile(filename):
                        # adapted from https://realpython.com/intro-to-python-threading/
                        x = threading.Thread(target=mode.playCallback, \
                            args = (filename,row,col), daemon = True)
                        x.start()


    def redrawAll(mode, canvas):
        mode.drawBoard(canvas)        
        if not mode.isRecording and not mode.isCreating:
            mode.drawRecordButton(canvas)
            mode.drawAutomateButton(canvas)
            mode.drawEffectsButton(canvas)
            mode.drawCreateButton(canvas)
            mode.drawHelpButton(canvas)
        elif not mode.isCreating:
            mode.drawRecordButton(canvas)
        elif not mode.isRecording:
            mode.drawCreateButton(canvas)
        

class EffectsPage(SoundboardPage):
    def appStarted(mode):
        super().appStarted()
        mode.soundboard = mode.app.soundboardPage.soundboard

        mode.reverbx1, mode.reverby1 = mode.width*50/60, mode.margin -10
        mode.reverbx2, mode.reverby2 = mode.reverbx1 + mode.width/8,  mode.reverby1 + 30


        mode.filx1, mode.fily1 = (mode.width*40/60, mode.margin -10)
        mode.filx2, mode.fily2 = (mode.filx1 + mode.width/8, mode.fily1 + 30)


        mode.loopx1, mode.loopy1 = (mode.width*30/60, mode.margin -10)
        mode.loopx2, mode.loopy2 = (mode.loopx1 + mode.width/8, mode.loopy1 +30)

        mode.trimx1, mode.trimy1 = (mode.width*20/60, mode.margin -10)
        mode.trimx2, mode.trimy2 = (mode.trimx1 + mode.width/8, mode.trimy1 +30)

        mode.dragging = ''

    def drawReverbButton(mode, canvas):
        canvas.create_rectangle(mode.reverbx1, mode.reverby1, 
                                mode.reverbx2, mode.reverby2, 
                                fill = "plum", width = 3)
        canvas.create_text((mode.reverbx1 + mode.reverbx2)/2, mode.reverby1+15, 
                        text = "Reverb", font = f"Times {14} bold")

    def drawFilterButton(mode, canvas):
        canvas.create_rectangle(mode.filx1, mode.fily1, mode.filx2, mode.fily2,
                                fill = "lightblue", width = 3)
        canvas.create_text((mode.filx1 + mode.filx2)/2, mode.fily1+15,
                        text = "Crop", font = f"Times {14} bold")

    def drawLoopButton(mode, canvas):
        canvas.create_rectangle(mode.loopx1, mode.loopy1, 
                                mode.loopx2, mode.loopy2,
                                fill = "orchid", width = 3)
        canvas.create_text((mode.loopx1 + mode.loopx2)/2, mode.loopy1+15,
                        text = "Loop", font = f"Times {14} bold")

    def drawTrimButton(mode, canvas):
        canvas.create_rectangle(mode.trimx1, mode.trimy1, 
                                mode.trimx2, mode.trimy2,
                                fill = "mistyrose", width = 3)
        canvas.create_text((mode.trimx1 + mode.trimx2)/2, mode.trimy1+15,
                        text = "Trim", font = f"Times {14} bold")
    
    def drawBackArrow(mode, canvas):
        canvas.create_rectangle(mode.width*3/60, mode.margin -10, 
                                mode.width*13/60, mode.margin +20,
                                fill = "white", width = 3)
        canvas.create_text(mode.width*8/60, mode.margin + 5, 
                        text = "Back", font = f"Times {14} bold")

    def mousePressed(mode, event):
        row, col = mode.getRowandCol(event.x, event.y)

        # clicked reverb button
        if (row, col) == (-1, -1):
            if event.x > mode.reverbx1 and event.x < mode.reverbx2 \
                and event.y > mode.reverby1 and event.y < mode.reverby2:
                mode.dragging = "reverb"

            # clicked filter button
            elif event.x > mode.filx1 and event.x < mode.filx2 \
                and event.y > mode.fily1 and event.y < mode.fily2:
                mode.dragging = 'filter'

            # clicked loop button
            elif event.x > mode.loopx1 and event.x < mode.loopx2 \
                and event.y > mode.loopy1 and event.y < mode.loopy2:
                mode.dragging = 'loop'

            # clicked trim button
            elif event.x > mode.trimx1 and event.x < mode.trimx2 \
                and event.y > mode.trimy1 and event.y < mode.trimy2:
                mode.dragging = 'trim'

        else:
            # clicked a square
            key = mode.soundboard.keys[row][col]
            path = \
            mode.getUserInput("Enter a .wav file to assign to key '" + key + "':")
            if path == None:
                return
            if (path != None):
                while not os.path.isfile(path):
                        path = mode.getUserInput\
                        ("Make sure the .wav file is in the same folder")
                        if (path == None):
                            return
                while (not path.endswith(".wav")):
                    path = mode.getUserInput\
                        ("Enter a .wav file \ to assign to key '" + key + "':")
                    if (path == None):
                        return
                    
            mode.soundboard.soundFiles[row][col] = path    
        
        # clicked back arrow
        if event.x > mode.width*3/60 and event.x < mode.width*13/60 and \
            event.y >  mode.margin -10 and event.y < mode.margin +20:
            mode.app.soundboardPage.soundboard = mode.soundboard
            mode.app.setActiveMode(mode.app.soundboardPage)


    def mouseDragged(mode, event):

        # clicked reverb button
        if mode.dragging == 'reverb':
            
            mode.reverbx1 = event.x
            mode.reverby1 = event.y
            mode.reverbx2 = mode.reverbx1 + mode.width/8
            mode.reverby2 = mode.reverby1 + 30


        # clicked filter button
        elif mode.dragging == "filter":
            mode.filx1 = event.x
            mode.fily1 = event.y
            mode.filx2 = mode.filx1 + mode.width/8
            mode.fily2 = mode.fily1 + 30

        # clicked loop button
        elif mode.dragging == 'loop':
            mode.loopx1 = event.x
            mode.loopy1 = event.y
            mode.loopx2 = mode.loopx1 + mode.width/8
            mode.loopy2 = mode.loopy1 + 30

        # clicked loop button
        elif mode.dragging == 'trim':
            mode.trimx1 = event.x
            mode.trimy1 = event.y
            mode.trimx2 = mode.trimx1 + mode.width/8
            mode.trimy2 = mode.trimy1 + 30


    def mouseReleased(mode, event):
        mode.reverbx1, mode.reverby1 = mode.width*50/60, mode.margin -10
        mode.reverbx2, mode.reverby2 = mode.reverbx1 + mode.width/8,  mode.reverby1 + 30
        mode.filx1, mode.fily1 = (mode.width*40/60, mode.margin -10)
        mode.filx2, mode.fily2 = (mode.filx1 + mode.width/8, mode.fily1 + 30)
        mode.loopx1, mode.loopy1 = (mode.width*30/60, mode.margin -10)
        mode.loopx2, mode.loopy2 = (mode.loopx1 + mode.width/8, mode.loopy1 +30)
        mode.trimx1, mode.trimy1 = (mode.width*20/60, mode.margin -10)
        mode.trimx2, mode.trimy2 = (mode.trimx1 + mode.width/8, mode.trimy1 +30)

        row, col = mode.getRowandCol(event.x, event.y)

        # not on a key
        if (row, col) == (-1, -1):
            return
        else:
            if mode.dragging == "reverb":
                if (mode.soundboard.soundFiles[row][col] != []):
                    outfile = Audio.reverb(mode.soundboard.soundFiles[row][col])
                    mode.soundboard.soundFiles[row][col] = outfile
            elif mode.dragging == "filter":
                if (mode.soundboard.soundFiles[row][col] != []):
                    outfile = Audio.crop(mode.soundboard.soundFiles[row][col])
                    mode.soundboard.soundFiles[row][col] = outfile
            
            elif mode.dragging == "loop":
                if (mode.soundboard.soundFiles[row][col] != []):
                    loopAmount = mode.getUserInput("How many times to loop?")
                    if loopAmount == None:
                        return
                    speed = mode.getUserInput("How fast to loop? (1 is speedy, 10 is slow)")
                    if speed == None:
                        return
                    outfile = Audio.loop(mode.soundboard.soundFiles[row][col], \
                        int(loopAmount), int(speed))
                    mode.soundboard.soundFiles[row][col] = outfile
            
            elif mode.dragging == 'trim':
                if (mode.soundboard.soundFiles[row][col] != []):
                    outfile = Audio.trimSilence(mode.soundboard.soundFiles[row][col])
                    mode.soundboard.soundFiles[row][col] = outfile
                
            

    def redrawAll(mode, canvas):
        mode.drawBoard(canvas)
        mode.drawFilterButton(canvas)
        mode.drawLoopButton(canvas)
        mode.drawReverbButton(canvas)
        mode.drawTrimButton(canvas)
        mode.drawBackArrow(canvas)


class AutomatePage(Mode):
    def appStarted(mode):
        mode.soundboard = mode.app.soundboardPage.soundboard
        mode.boxes = []
        mode.bolds = [1,1,1,1,1]
        h = mode.height/20
        for i in range(0, 15, 3):
            mode.boxes.append((mode.width/4, mode.height/6 + h*i,
                    mode.width/4*3, mode.height/100*23 + h*(i+1)))
        
        mode.selected = False
        mode.selectedBox = 0
        mode.beat = DefaultBeat(mode.soundboard)
        mode.soundstring = ''
        
        mode.sounds = set()
        for row in range (len(mode.soundboard.soundFiles)):
            for col in range(len(mode.soundboard.soundFiles[0])):
                if mode.soundboard.soundFiles[row][col] != []:
                    mode.sounds.add(mode.soundboard.soundFiles[row][col])
                    mode.soundstring += str(mode.soundboard.soundFiles[row][col]) + ', '
        mode.soundstring = '(' + mode.soundstring[:-2] + ')'

    def drawStartButton(mode, canvas):
        canvas.create_oval(mode.width*9/12, mode.height/22, 
                                mode.width*11/12, mode.height/10,
                                width = 3)
        canvas.create_text(mode.width*10/12, mode.height/14, 
                        text = "Start", font = f"Times {14} bold")

    def drawBackArrow(mode, canvas):
        canvas.create_rectangle(mode.width*3/60, 20, 
                                mode.width*13/60, 50,
                                fill = "white", width = 3)
        canvas.create_text(mode.width*8/60, 35, 
                        text = "Back", font = f"Times {14} bold")
    
    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2, mode.height/10, text = "Automate", 
            font = f"Impact {mode.width//18}")
        
        mode.drawStartButton(canvas)
        mode.drawBackArrow(canvas)
       
        for i in range(5):
            x1, y1, x2, y2 = mode.boxes[i]
            canvas.create_rectangle(x1, y1, x2, y2, width = mode.bolds[i])
            if i==0:
                text = "Simple Beat: 2 Sounds"
            elif i==1:
                text = "Dance Beat: 3 Sounds"
            elif i==2:
                text = "Syncopated Beat 3: Sounds"
            elif i==3:
                text = "Hip Hop Beat 4 Sounds"
            elif i==4:
                text = "CREATION"
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text = text)
        
        canvas.create_rectangle(mode.width/40*31, mode.height/6 + mode.height/60*37,
                    mode.width/20*18, mode.height/100*23 + mode.height/60*38,
                    width = 2)
        canvas.create_text(mode.width/80*67, mode.height/6 + mode.height/120*76,
                        text = "Play")
        canvas.create_text(mode.width/80*67, mode.height/6 + mode.height/120*80,
                        text = "Creation")


    def mousePressed(mode, event):
        mode.soundstring = ''        
        mode.sounds = set()
        for row in range (len(mode.soundboard.soundFiles)):
            for col in range(len(mode.soundboard.soundFiles[0])):
                if mode.soundboard.soundFiles[row][col] != []:
                    mode.sounds.add(mode.soundboard.soundFiles[row][col])
                    mode.soundstring += str(mode.soundboard.soundFiles[row][col]) + ', '
        mode.soundstring = '(' + mode.soundstring[:-2] + ')'
                    
        
        for i in range(5):
            x1, y1, x2, y2 = mode.boxes[i]
            if event.x>x1 and event.x<x2 and event.y>y1 and event.y<y2:

                if mode.selected and mode.selectedBox == i:
                    x1a, y1a, x2a, y2a = mode.boxes[mode.selectedBox]
                    x1a -= mode.width/100
                    x2a += mode.width/100
                    y1a -= mode.height/100
                    y2a += mode.height/100
                    mode.boxes[mode.selectedBox] = (x1a, y1a, x2a, y2a)
                    mode.bolds[mode.selectedBox] = 1
                    mode.selected = False

                else:
                    x1 += mode.width/100
                    x2 -= mode.width/100
                    y1 += mode.height/100
                    y2 -= mode.height/100
                    mode.boxes[i] = (x1, y1, x2, y2)
                    mode.bolds[i] = 3
                    if mode.selected:
                        x1a, y1a, x2a, y2a = mode.boxes[mode.selectedBox]
                        x1a -= mode.width/100
                        x2a += mode.width/100
                        y1a -= mode.height/100
                        y2a += mode.height/100
                        mode.boxes[mode.selectedBox] = (x1a, y1a, x2a, y2a)
                        mode.bolds[mode.selectedBox] = 1
                    mode.selected = True
                    mode.selectedBox = i

        # clicked start
        if mode.selected:
            if event.x > mode.width*9/12 and event.y > mode.height/22 and \
                    event.x < mode.width*11/12 and event.y < mode.height/10:
                if mode.selectedBox==4:
                    mode.creation()
                else:
                    mode.automate()
        
        # clicked play original
        if mode.selectedBox==4 and \
                event.x > mode.width/40*31 and \
                event.y > mode.height/6 + mode.height/60*37 and \
                event.x < mode.width/20*18 and \
                event.y < mode.height/100*23 + mode.height/60*38:

            if mode.app.soundboardPage.listtimes != []:
                mode.app.soundboardPage.getCreatedBeat()
                creationPage = CreationSoundboardPage()
                mode.app.setActiveMode(creationPage)
       
        # clicked back arrow
        if event.x > mode.width*3/60 and event.x < mode.width*13/60 and \
            event.y > 20 and event.y < 50:
            mode.app.setActiveMode(mode.app.soundboardPage)

    def creation(mode):
        for sound in mode.app.soundboardPage.setSounds:
            output = mode.getUserInput('Enter file for ' + sound + ', a for automate '+ mode.soundstring)
            if output == None:
                return
            elif output == 'a':
                output = mode.findMatchFile(sound)
            else:
                while output not in mode.sounds:
                    if output == None:
                        return
                    elif output == 'a':
                        output = mode.findMatchFile(sound)
                    else:
                        output = mode.getUserInput\
                            ("Make sure the file is on soundboard "+ mode.soundstring)
            for i in range(len(mode.app.soundboardPage.listsounds)):
                if mode.app.soundboardPage.listsounds[i] == sound:
                    mode.app.soundboardPage.listsounds[i] = output
        
        if mode.app.soundboardPage.listtimes != []:
            mode.app.soundboardPage.getCreatedBeat()
            creationPage = CreationSoundboardPage()
            mode.app.setActiveMode(creationPage)

    def findMatchFile(mode, path):
        listsounds = mode.app.soundboardPage.listsounds
        final = path
        freq = Audio.getFrequency(path)
        if len(mode.sounds) > 1:
            d = 100000
            #find closest freq
            for sound in mode.sounds:
                if abs(Audio.getFrequency(sound)-freq) < d and \
                    abs(Audio.getFrequency(sound)-freq) > 0:
                    final = sound
                    d = abs(Audio.getFrequency(sound)-freq)
        return final
            

    def automate(mode):
        if mode.selectedBox == 0:            
            mode.beat = DefaultBeat1(mode.soundboard)
            
            outputkick = mode.getUserInput("Enter kick file, enter 'a' for automate " + mode.soundstring)
            if outputkick == None:
                return
            elif outputkick == 'a':
                mode.beat.getKick()
            else:
                while outputkick not in mode.sounds:
                    if outputkick == None:
                        return
                    elif outputkick == 'a':
                        mode.beat.getKick()
                    else:
                        outputkick = mode.getUserInput\
                            ("Make sure the kick file is on soundboard " + mode.soundstring)
                mode.beat.kick = outputkick
            
            outputsnare = mode.getUserInput("Enter snare file, press 'a' for automate "+ mode.soundstring)

            if outputsnare == None:
                return
            elif outputsnare == 'a':
                mode.beat.getSnare()
            else:
                while outputsnare not in mode.sounds:
                    if outputsnare == None:
                        return
                    elif outputsnare == 'a':
                        mode.beat.getSnare()
                    else:
                        outputsnare = mode.getUserInput\
                            ("Make sure the snare file is on soundboard "+ mode.soundstring)
                mode.beat.snare = outputsnare

        elif mode.selectedBox == 1:
            mode.beat = DefaultBeat2(mode.soundboard)

            outputkick = mode.getUserInput("Enter kick file, enter 'a' for automate "+ mode.soundstring)
            if outputkick == None:
                return
            elif outputkick == 'a':
                mode.beat.getKick()
            else:
                while outputkick not in mode.sounds:
                    if outputkick == None:
                        return
                    elif outputkick == 'a':
                        mode.beat.getKick()
                    else:
                        outputkick = mode.getUserInput\
                            ("Make sure the kick file is on soundboard "+ mode.soundstring)
                mode.beat.kick = outputkick
            
            outputsnare = mode.getUserInput("Enter snare file, press 'a for automate "+ mode.soundstring)

            if outputsnare == None:
                return
            elif outputsnare == 'a':
                mode.beat.getSnare()
            else:
                while outputsnare not in mode.sounds:
                    if outputsnare == None:
                        return
                    elif outputsnare == 'a':
                        mode.beat.getSnare()
                    else:
                        outputsnare = mode.getUserInput\
                            ("Make sure the snare file is in on soundboard "+ mode.soundstring)
                mode.beat.snare = outputsnare
            
            outputclosed = mode.getUserInput("Enter closed hi hat file, enter 'a' for automate "+ mode.soundstring)
            if outputclosed == None:
                return
            elif outputclosed == 'a':
                mode.beat.getClosedHiHat()
            else:
                while outputclosed not in mode.sounds:
                    if outputclosed == None:
                        return
                    elif outputclosed == 'a':
                        mode.beat.getClosedHiHat()
                    else:
                        outputclosed = mode.getUserInput\
                            ("Make sure the closedhihat file is on soundboard "+ mode.soundstring)
                mode.beat.closedhihat = outputclosed


        elif mode.selectedBox == 2:
            mode.beat = DefaultBeat3(mode.soundboard)

            outputkick = mode.getUserInput("Enter kick file, enter 'a' for automate "+ mode.soundstring)
            if outputkick == None:
                return
            elif outputkick == 'a':
                mode.beat.getKick()
            else:
                while outputkick not in mode.sounds:
                    if outputkick == None:
                        return
                    elif outputkick == 'a':
                        mode.beat.getKick()
                    else:
                        outputkick = mode.getUserInput\
                            ("Make sure the kick file is on soundboard "+ mode.soundstring)
                mode.beat.kick = outputkick
            
            outputsnare = mode.getUserInput("Enter snare file, press 'a for automate "+ mode.soundstring)

            if outputsnare == None:
                return
            elif outputsnare == 'a':
                mode.beat.getSnare()
            else:
                while outputsnare not in mode.sounds:
                    if outputsnare == None:
                        return
                    elif outputsnare == 'a':
                        mode.beat.getSnare()
                    else:
                        outputsnare = mode.getUserInput\
                            ("Make sure the snare file is on soundboard "+ mode.soundstring)
                mode.beat.snare = outputsnare
            
            outputclosed = mode.getUserInput("Enter closed hi hat file, enter 'a' for automate "+ mode.soundstring)
            if outputclosed == None:
                return
            elif outputclosed == 'a':
                mode.beat.getClosedHiHat()
            else:
                while outputclosed not in mode.sounds:
                    if outputclosed == None:
                        return
                    elif outputclosed == 'a':
                        mode.beat.getClosedHiHat()
                    else:
                        outputclosed = mode.getUserInput\
                            ("Make sure the kick file is in on soundboard "+ mode.soundstring)
                    mode.beat.closedhihat = outputclosed

            

        elif mode.selectedBox == 3:
            mode.beat = DefaultBeat4(mode.soundboard)

            outputkick = mode.getUserInput("Enter kick file, enter 'a' for automate "+ mode.soundstring)
            if outputkick == None:
                return
            elif outputkick == 'a':
                mode.beat.getKick()
            else:
                while outputkick not in mode.sounds:
                    if outputkick == None:
                        return
                    elif outputkick == 'a':
                        mode.beat.getKick()
                    else:
                        outputkick = mode.getUserInput\
                            ("Make sure the kick file is on soundboard "+ mode.soundstring)
                mode.beat.kick = outputkick
            
            outputsnare = mode.getUserInput("Enter snare file, press 'a for automate "+ mode.soundstring)
            if outputsnare == None:
                return
            elif outputsnare == 'a':
                mode.beat.getSnare()
            else:
                while outputsnare not in mode.sounds:
                    if outputsnare == None:
                        return
                    elif outputsnare == 'a':
                        mode.beat.getSnare()
                    else:
                        outputsnare = mode.getUserInput\
                            ("Make sure the snare file is on soundboard "+ mode.soundstring)
                mode.beat.snare = outputsnare
            
            outputclosed = mode.getUserInput("Enter closed hi hat file, enter 'a' for automate "+ mode.soundstring)
            if outputclosed == None:
                return
            elif outputclosed == 'a':
                mode.beat.getClosedHiHat()
            else:
                while outputclosed not in mode.sounds:
                    if outputclosed == None:
                        return
                    elif outputclosed == 'a':
                        mode.beat.getClosedHiHat()
                    else:
                        outputclosed = mode.getUserInput\
                            ("Make sure the closedhihat file is on soundboard "+ mode.soundstring)
                mode.beat.closedhihat = outputclosed

            outputopen = mode.getUserInput("Enter open hi hat file, enter 'a' for automate "+ mode.soundstring)
            if outputopen == None:
                return
            elif outputopen == 'a':
                mode.beat.getOpenHiHat()
            else:
                while outputopen not in mode.sounds:
                    if outputopen == None:
                        return
                    elif outputopen == 'a':
                        mode.beat.getOpenHiHat()
                    else:
                        outputopen = mode.getUserInput\
                            ("Make sure the openhihat file is on soundboard "+ mode.soundstring)
                mode.beat.openhihat = outputopen


        automatedSBPage = AutomatedSoundboardPage()
        mode.app.setActiveMode(automatedSBPage)

class AutomatedSoundboardPage(SoundboardPage):
    def appStarted(mode):
        super().appStarted()
        mode.soundboard = mode.app.soundboardPage.soundboard
        
        mode.beat = mode.app.automatePage.beat
  
        if mode.beat.kick != None and len(mode.beat.kickTimes) != 0:           
            mode.rkick, mode.ckick = mode.soundboard.getRowandColfromFile(mode.beat.kick)
        if mode.beat.snare != None and len(mode.beat.snareTimes) != 0 :          
            mode.rsnare, mode.csnare = mode.soundboard.getRowandColfromFile(mode.beat.snare)
        if len(mode.beat.openhihatTimes) != 0 and mode.beat.openhihat != None:            
            mode.ropenhihat, mode.copenhihat = mode.soundboard.getRowandColfromFile(mode.beat.openhihat)

        if len(mode.beat.closedhihatTimes) != 0 and mode.beat.closedhihat != None:                       
            mode.rclosedhihat, mode.cclosedhihat = mode.soundboard.getRowandColfromFile(mode.beat.closedhihat)
        if len(mode.beat.shakerTimes) != 0 and mode.beat.shaker != None:            
            mode.rshaker, mode.cshaker = mode.soundboard.getRowandColfromFile(mode.beat.shaker)
        
        mode.app.timerDelay = mode.beat.timer
        mode.i = 0


    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    # and https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
    def playCallback2(mode, path, row, col):
        if len(sys.argv) < 2:
            print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
            #sys.exit(-1)

        wf = wave.open(path, 'rb')

        p = pyaudio.PyAudio()

        mode.soundboard.pressed[row][col] = True

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        stream.start_stream()

        data = wf.readframes(800)

        # int(RATE / CHUNK * RECORD_SECONDS)
        for i in range(0, int(44100 / 800 * 0.5)):
            if not mode.soundboard.pressed[row][col]:
                break
            stream.write(data)
            data = wf.readframes(800)

        stream.stop_stream()
        mode.soundboard.pressed[row][col] = False
        stream.close()
        wf.close()

        p.terminate()


    def timerFired(mode):

        mode.i += 1

        if mode.beat.kick != [] and mode.beat.kick != None and os.path.isfile(mode.beat.kick):
            if (mode.i%32 in mode.beat.kickTimes):
                # adapted from https://realpython.com/intro-to-python-threading/
                a = threading.Thread(target=mode.playCallback2, args = (mode.beat.kick, mode.rkick, mode.ckick), daemon = True)                    
                a.start()           
        
        if mode.beat.snare != []  and mode.beat.snare != None and os.path.isfile(mode.beat.snare):
            if (mode.i%32 in mode.beat.snareTimes):
                a = threading.Thread(target=mode.playCallback2, args = (mode.beat.snare,mode.rsnare,mode.csnare), daemon = True)                    
                a.start()

        if mode.beat.openhihat != []  and mode.beat.openhihat != None and os.path.isfile(mode.beat.openhihat):
            if (mode.i%32 in mode.beat.openhihatTimes):
                # adapted from https://realpython.com/intro-to-python-threading/
                a = threading.Thread(target=mode.playCallback2, args = (mode.beat.openhihat, mode.ropenhihat, mode.copenhihat), daemon = True)                    
                a.start() 
        
        if mode.beat.closedhihat != [] and mode.beat.closedhihat != None and os.path.isfile(mode.beat.closedhihat):
            if (mode.i%32 in mode.beat.closedhihatTimes):
                # adapted from https://realpython.com/intro-to-python-threading/
                a = threading.Thread(target=mode.playCallback2, args = (mode.beat.closedhihat, mode.rclosedhihat, mode.cclosedhihat), daemon = True)                    
                a.start() 

        if mode.beat.shaker != None and mode.beat.shaker != None and os.path.isfile(mode.beat.shaker):           
            if (mode.i%32 in mode.beat.shakerTimes):
                # adapted from https://realpython.com/intro-to-python-threading/
                a = threading.Thread(target=mode.playCallback2, args = (mode.beat.shaker,mode.rshaker,mode.cshaker), daemon = True)                    
                a.start()

    def mousePressed(mode, event):
        #record button
        if event.x > mode.width*9/12 and event.x < mode.width*11/12 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:

                if mode.isRecording:
                    mode.isRecording = False
                else:
                    output = mode.getUserInput("Name your file: ")
                    output = output + ".wav"
                    # adapted from https://realpython.com/intro-to-python-threading/
                    y = threading.Thread(target=mode.voiceRecord, args = (output,), daemon = True)                    
                    y.start()

        if not mode.isRecording:
            # exit button
            if event.x > mode.width*1/12 and event.x < mode.width*3/12 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:
                mode.app.setActiveMode(mode.app.automatePage)

    def drawExitButton(mode, canvas):
        canvas.create_oval(mode.width*1/12, mode.margin -10, 
                                mode.width*3/12, mode.margin +20,
                                fill = "red", width = 3)
        canvas.create_text(mode.width*2/12, mode.margin + 5, 
                        text = "Exit", font = f"Times {14} bold")
        

    def redrawAll(mode, canvas):
        mode.drawBoard(canvas)
        mode.drawRecordButton(canvas)
        if not mode.isRecording:
            mode.drawExitButton(canvas)

class CreationSoundboardPage(SoundboardPage):
    def appStarted(mode):
        super().appStarted()
        mode.soundboard = mode.app.soundboardPage.soundboard
        # adapted from https://realpython.com/intro-to-python-threading/
        x = threading.Thread(target=mode.app.soundboardPage.playDefaultBeat, \
                args = (), daemon = True)                    
        x.start()

    def drawRepeatButton(mode, canvas):
        canvas.create_oval(mode.width*6/12, mode.margin -10, 
                                mode.width*8/12, mode.margin +20,
                                fill = "red", width = 3)
        canvas.create_text(mode.width*7/12, mode.margin + 5, 
                        text = "Repeat", font = f"Times {14} bold")
        
    def mousePressed(mode, event):
        #record button
        if event.x > mode.width*9/12 and event.x < mode.width*11/12 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:

                if mode.isRecording:
                    mode.isRecording = False
                else:
                    output = mode.getUserInput("Name your file: ")
                    output = output + ".wav"
                    # adapted from https://realpython.com/intro-to-python-threading/
                    y = threading.Thread(target=mode.voiceRecord, args = (output,), daemon = True)                    
                    y.start()
        # repeat
        if event.x > mode.width*6/12 and event.x < mode.width*8/12 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:
            mode.app.soundboardPage.getCreatedBeat()
            x = threading.Thread(target=mode.app.soundboardPage.playDefaultBeat, \
                args = (), daemon = True)                    
            x.start()

        if not mode.isRecording:
            # exit button
            if event.x > mode.width*1/12 and event.x < mode.width*3/12 \
                and event.y > mode.margin -10 and event.y < mode.margin +20:
                mode.app.setActiveMode(mode.app.automatePage)

    def drawExitButton(mode, canvas):
        canvas.create_oval(mode.width*1/12, mode.margin -10, 
                                mode.width*3/12, mode.margin +20,
                                fill = "red", width = 3)
        canvas.create_text(mode.width*2/12, mode.margin + 5, 
                        text = "Exit", font = f"Times {14} bold")
        

    def redrawAll(mode, canvas):
        mode.drawBoard(canvas)
        mode.drawRecordButton(canvas)
        mode.drawRepeatButton(canvas)
        if not mode.isRecording:
            mode.drawExitButton(canvas)

# adapted from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
class HelpPage(Mode):
    def redrawAll(mode, canvas):
        mode.drawBackButton(canvas)
        canvas.create_text(mode.width/2, mode.height/10, \
            text="Help", font='Impact 30 bold')
        
        text = '''* Click on boxes to enter wave files
                    * Use keys to play sounds
                    * Click voice record to record from microphone
                    * Add effects to sounds (reverb, loop, crop 
                    snippet from beginning, trim silence)                    
                    * Automate default beats from inputted sounds
                    * Create a beat and use it as a template to make
                    something new with different sounds
                    * [Match sounds manually or enter 'a' for
                    automatic match]'''

        y = mode.height/5
        for line in text.splitlines():
            canvas.create_text(mode.width/2, y, text=line.strip(), font='Times 20')
            y += mode.height/13

    def drawBackButton(mode, canvas):
        canvas.create_rectangle(mode.width*3/60, 10, 
                                mode.width*9/60, 40,
                                fill = "white", width = 3)
        canvas.create_text(mode.width*6/60, 25, 
                        text = "Back", font = f"Times {14} bold")

    def mousePressed(mode, event):
        if event.x > mode.width*3/60 and event.y > 10 \
                and event.x < mode.width*9/60 and 40:
                    mode.app.setActiveMode(mode.app.soundboardPage)