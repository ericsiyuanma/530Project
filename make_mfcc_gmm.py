#! /usr/bin/env python

import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff, append
import numpy as np
from numpy import arange
from demo_waveform_plot import get_waveform_plot
from demo_waveform_plot import set_xlabels_sample2time
import matplotlib.pyplot as plt


class Mixture:
    def __init__(self, weight, mean, covar):
        self.weight = weight
        self.mean = mean
        self.covar = covar


def plots(mode, mfccs, mfccs_append, source_filename, samplerate, hop_s, frames_read):
    from sklearn import mixture
    fig = plt.figure()
    plt.rc('lines', linewidth='.8')
    wave = plt.axes([0.1, 0.75, 0.8, 0.19])

    get_waveform_plot(source_filename, samplerate, block_size=hop_s, ax=wave)
    wave.xaxis.set_visible(False)
    wave.yaxis.set_visible(False)

    # compute first and second derivatives
    if mode in ["delta", "ddelta"]:
        mfccs = diff(mfccs, axis=0)
    if mode == "ddelta":
        mfccs = diff(mfccs, axis=0)

    all_times = arange(mfccs.shape[0]) * hop_s  # this is milliseconds
    n_coeffs = mfccs.shape[1]

    X = np.zeros((len(mfccs_append), 2))
    for i in range(X.shape[0]):
        X[i, 0] = i
        X[i, 1] = mfccs_append[i]

    num_components = 10
    stuff = np.concatenate(mfccs, axis=0)
    print(len(mfccs_append))
    gmm = mixture.GaussianMixture(n_components=num_components, covariance_type='full',
                                  max_iter=75).fit(X)

    print(gmm.covariances_)
    mixtures = []
    for n in range(0, num_components):
        mixtures.append(Mixture(gmm.weights_[n], gmm.means_[n], gmm.covariances_[n][:2, :2]))

    for mixture in mixtures:
        print(mixture.weight)
        print(mixture.mean)
        print(mixture.covar)
        print()

    # print(all_times,n_coeffs)
    for i in range(n_coeffs):
        ax = plt.axes([0.1, 0.75 - ((i + 1) * 0.65 / n_coeffs), 0.8, 0.65 / n_coeffs], sharex=wave)
        ax.xaxis.set_visible(False)
        ax.set_yticks([])
        ax.set_ylabel('%d' % i)
        ax.plot(all_times, mfccs.T[i])

    # add time to the last axis
    set_xlabels_sample2time(ax, frames_read, samplerate)

    # plt.ylabel('spectral descriptor value')
    ax.xaxis.set_visible(True)
    title = 'MFCC for %s' % source_filename
    if mode == "delta":
        title = mode + " " + title
    elif mode == "ddelta":
        title = "double-delta" + " " + title
    wave.set_title(title)
    plt.show()


def calculate(filename):
    n_filters = 40  # must be 40 for mfcc
    n_coeffs = 13

    source_filename = filename
    samplerate = 0
    win_s = 64
    hop_s = win_s // 4
    mode = "default"

    s = source(source_filename, samplerate, hop_s)
    samplerate = s.samplerate
    p = pvoc(win_s, hop_s)
    m = mfcc(win_s, n_filters, n_coeffs, samplerate)

    mfccs = zeros([n_coeffs, ])
    mfccs_append = []
    frames_read = 0
    while True:
        samples, read = s()
        spec = p(samples)
        mfcc_out = m(spec)
        mfccs = vstack((mfccs, mfcc_out))
        mfccs_append = append(mfccs_append, mfcc_out)
        frames_read += read
        if read < hop_s: break

    plots(mode, mfccs, mfccs_append, source_filename, samplerate, hop_s, frames_read)


calculate("sneaking.wav")
