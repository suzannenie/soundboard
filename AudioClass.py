# This file contains the static functions pertaining to audio

import random, math, copy
import aubio
from aubio import source, pitch
import numpy as np
import pyaudio
import audioop
import wave
import time
from pysndfx import AudioEffectsChain
# from http://sox.sourceforge.net/
import sox
import threading


class Audio(object):

    # adapted from https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
    @staticmethod
    def trimSilence(filename):

        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'rb')
        chunk = 300
        frames = []
        
        data = wf.readframes(chunk)

        silence = True
        while len(data) > 0:
            data = wf.readframes(chunk)

            # adapted from https://docs.python.org/2/library/audioop.html#audioop.avg

            if silence:
                if (audioop.avg(data, 4) > 160000):
                    silence = False
                    print('here')      
                    frames.append(data)          
            else:
                frames.append(data)
            # if (audioop.avg(data, 4) > 160000):
            #     frames.append(data)
                
                 
        outfile = wave.open(filename[:-4] + '_trimmed.wav', 'wb')
        outfile.setnchannels(2)
        outfile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        outfile.setframerate(44100)
        outfile.writeframes(b''.join(frames))
        outfile.close()
        return filename[:-4] + '_trimmed.wav'

        # adapted from https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
    @staticmethod
    def trimAllSilence(filename):

        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'rb')
        chunk = 300
        frames = []
        
        data = wf.readframes(chunk)

        silence = True
        while len(data) > 0:
            data = wf.readframes(chunk)

            # adapted from https://docs.python.org/2/library/audioop.html#audioop.avg

            if (audioop.avg(data, 4) > 160000):
                frames.append(data)
                
                 
        outfile = wave.open(filename[:-4] + '_trimmed.wav', 'wb')
        outfile.setnchannels(2)
        outfile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        outfile.setframerate(44100)
        outfile.writeframes(b''.join(frames))
        outfile.close()
        return filename[:-4] + '_trimmed.wav'

    def flanger( file ):
        pass

    # from https://github.com/carlthome/python-audio-effects
    #echoes 3 times lol
    @staticmethod
    def reverb(infile):
        fx = (
            AudioEffectsChain()
            .highshelf()
            .reverb()
            .phaser()
            .delay()
            .lowshelf()
        )
        outfile = infile[:-4] + '_reverb.wav'

        # Apply phaser and reverb directly to an audio file.
        fx(infile, outfile)
        return outfile

    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    @staticmethod
    def play(path):
        wf = wave.open(path, 'rb')

        p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()

    #modified from: https://git.aubio.org/?p=aubio.git;a=blob;f=python/demos/
    # demo_pitch.py;h=81f17cd4b3eed408abb31adbccd1ba39296dbacd;hb=c3c630598784
    # 8593034cb34501a9d3bc7afd6e8c
    def getFrequency(filename):
        downsample = 8
        samplerate = 44100 // downsample
        win_s = 4096 // downsample # fft size
        hop_s = 512  // downsample # hop size
        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        tolerance = 0.8
        pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("freq")
        pitch_o.set_tolerance(tolerance)
        pitches = []
        confidences = []
        # total number of frames read
        total_frames = 0
        counter = 0
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break
        letterList = []
        newPitches = []
        for index in range(0, len(pitches)):
            totalFreq = 0
            if(index+5 <= len(pitches)):
                for freq in range(index, index+5):
                    totalFreq += pitches[freq]
                averageFreq = totalFreq/5
                if averageFreq > 0:
                    newPitches.append(averageFreq)
            else:
                counter = 0
                for index in range(index, len(pitches)):
                    totalFreq += pitches[freq]
                    counter += 1
                averageFreq = totalFreq/counter
                newPitches.append(averageFreq)
        total = 0
        divisor = 0
        for pi in newPitches:
            total+=pi
            divisor +=1
        if divisor == 0:
            return 0
        return (total/divisor)

    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    @staticmethod
    def loop (filename, loopAmount, speed):
        p = pyaudio.PyAudio()
        chunk = 800
        w = wave.open('silence.wav', 'rb')
        silentframes = []
        data = w.readframes(chunk)
        while len(data) > 0:
            data = w.readframes(chunk)
            silentframes.append(data)

        wf = wave.open(filename, 'rb')        
        frames = []
        
        data = wf.readframes(chunk)

        while len(data) > 0:
            data = wf.readframes(chunk)
            frames.append(data)
                
        newFrames = frames + speed*silentframes
        loopedFrames = loopAmount * newFrames       
        outfile = wave.open(filename[:-4] + '_loop.wav', 'wb')
        outfile.setnchannels(wf.getnchannels())
        outfile.setsampwidth(wf.getsampwidth())
        outfile.setframerate(wf.getframerate())
        outfile.writeframes(b''.join(loopedFrames))
        outfile.close()
        return filename[:-4] + '_loop.wav'

    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    @staticmethod
    def getSoundBytes(sound):
        p = pyaudio.PyAudio()
        frames = []
        chunk = 300
        wf = wave.open(sound, 'rb')
        data = wf.readframes(chunk)
        while len(data) > 0:            
            frames.append(data)
            data = wf.readframes(chunk)
        return frames

    # adapted from https://people.csail.mit.edu/hubert/pyaudio/docs/
    @staticmethod
    def crop(filename):
        p = pyaudio.PyAudio()
        wf = wave.open(filename, 'rb')
        chunk = 800
        frames = []
        
        data = wf.readframes(chunk)

        for i in range(0, int(44100 / chunk * 0.15)):
            data = wf.readframes(chunk)
            frames.append(data)
            # adapted from https://docs.python.org/2/library/audioop.html#audioop.avg
            # if (audioop.avg(data, 4) > 160000):
            #     frames.append(data)
    
        outfile = wave.open(filename[:-4] + '_crop.wav', 'wb')
        outfile.setnchannels(wf.getnchannels())
        outfile.setsampwidth(wf.getsampwidth())
        outfile.setframerate(wf.getframerate())
        outfile.writeframes(b''.join(frames))
        outfile.close()
        return filename[:-4] + '_crop.wav'

