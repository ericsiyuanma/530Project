#! /usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from aubio import source
from aubio import pitch as pitch_aubio

from lmfit.models import PolynomialModel
from pydub import AudioSegment
from change_tempo import change_tempo_file


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def read_pitch(filename):

    filename = filename

    sound = AudioSegment.from_wav(filename)

    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)

    trimmed_sound = sound[start_trim:duration - end_trim]

    duration = len(trimmed_sound)

    time_factor = round(duration / 1000, 2)

    #print("LENGTH IS %f" % duration)
    #print("TIME FACTOR  IS %f" % time_factor)

    trimmed_sound.export("passcode_og.wav", format="wav")

    change_tempo_file("passcode_og.wav", "passcode.wav", time_factor)

    downsample = 1
    samplerate = 44100 // downsample
    win_s = 4096 // downsample
    hop_s = 512 // downsample

    s = source("passcode.wav", samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch_aubio("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break
    if 0: sys.exit(0)

    y = list(filter(lambda a: a != 0.0, pitches))

    y = np.array([int(i) for i in y])
    x = np.array(list(range(0, len(y))))

    mod = PolynomialModel(7)
    pars = mod.guess(y, x=x)
    out = mod.fit(y, pars, x=x)

    curved_points = out.best_fit
    rounded_list = [round(elem, 0) for elem in y]

    ydiff = np.diff(rounded_list)
    np.all(ydiff[0] == ydiff)
    # print(ydiff)

    plt.plot(x, y, 'bo')
    plt.plot(x, out.init_fit, 'k--')
    plt.plot(x, out.best_fit, 'r-')
    plt.show()
    return y, curved_points
