#! /usr/bin/env python

import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff, append
from sklearn import mixture
import numpy as np
from sklearn.externals import joblib
from draw_gmm import plot_gmm

n_filters = 40  # must be 40 for mfcc
n_coeffs = 13

if len(sys.argv) < 2:
    print("Usage: %s <source_filename> [samplerate] [win_s] [hop_s] [mode]" %
          sys.argv[0])
    print(
        "  where [mode] can be 'delta' or 'ddelta' for first and second derivatives")
    sys.exit(1)

source_filename = sys.argv[1]

if len(sys.argv) > 2:
    samplerate = int(sys.argv[2])
else:
    samplerate = 0
if len(sys.argv) > 3:
    win_s = int(sys.argv[3])
else:
    win_s = 512
if len(sys.argv) > 4:
    hop_s = int(sys.argv[4])
else:
    hop_s = win_s // 4
if len(sys.argv) > 5:
    mode = sys.argv[5]
else:
    mode = "default"

samplerate = 0
if len(sys.argv) > 2: samplerate = int(sys.argv[2])

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

# do plotting
from numpy import arange
from demo_waveform_plot import get_waveform_plot
from demo_waveform_plot import set_xlabels_sample2time
import matplotlib.pyplot as plt

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
gmm = mixture.GaussianMixture(n_components=num_components, covariance_type='diag',
                              max_iter=75).fit(X)

for n in range(0,num_components):
    print("WEIGHT for MIXTURE %f " % n)
    print(gmm.weights_[n])
    print("MEAN for MIXTURE %f " % n)
    print(gmm.means_[n, :13])
    print("VARIANCE for MIXTURE %f " % n)
    print(np.diag(gmm.covariances_[n][:1]))


#print(all_times,n_coeffs)
for i in range(n_coeffs):
    ax = plt.axes ( [0.1, 0.75 - ((i+1) * 0.65 / n_coeffs),  0.8, 0.65 / n_coeffs], sharex = wave )
    ax.xaxis.set_visible(False)
    ax.set_yticks([])
    ax.set_ylabel('%d' % i)
    ax.plot(all_times, mfccs.T[i])

# add time to the last axis
set_xlabels_sample2time( ax, frames_read, samplerate)

#plt.ylabel('spectral descriptor value')
ax.xaxis.set_visible(True)
title = 'MFCC for %s' % source_filename
if mode == "delta": title = mode + " " + title
elif mode == "ddelta": title = "double-delta" + " " + title
wave.set_title(title)
plt.show()
