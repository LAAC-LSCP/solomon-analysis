#!/usr/bin/env python3
import os
import pandas as pd
import sys
import multiprocessing as mp
import numpy as np
from functools import partial
import sox
import traceback

import wave
import numpy as np
from scipy.fftpack import fft, ifft

from matplotlib import pyplot as plt

from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager

project = ChildProject(sys.argv[1])
project.read()

interval_length = 5*60

def get_audio_duration(filename):
    if not os.path.exists(filename):
        return 0

    duration = 0
    try:
        duration = sox.file_info.duration(filename)
    except:
        pass

    return duration

def read_wav(filename, start_s, length_s):
    fp = wave.open(filename)
    samples = fp.getnframes()
    sampling_rate = fp.getframerate()
    audio = fp.readframes(samples)

    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16, offset = start_s*sampling_rate, count=length_s*sampling_rate+1)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

    max_int16 = 2**15
    audio_normalised = audio_as_np_float32 / max_int16

    return audio_normalised, sampling_rate

def calculate_shift(file1, file2, start, interval):
    ref, ref_rate = read_wav(file1, start, interval)
    test, test_rate = read_wav(file2, start, interval)

    if ref_rate != test_rate:
        raise Exception('audios do not match')

    sampling_rate = ref_rate

    downsampled_rate = 400
    ref = ref[::int(sampling_rate/downsampled_rate)]
    test = test[::int(sampling_rate/downsampled_rate)]

    ref_padded = np.concatenate((np.zeros(len(ref)-1), ref))
    test_padded = np.concatenate((test, np.zeros(len(ref)-len(test)+len(ref)-1)))

    ref_fft = fft(ref_padded)
    test_fft = fft(test_padded)

    cross_spectral_density = ref_fft*np.conj(test_fft)
    cross_correlations = ifft(cross_spectral_density)

    mag_cross_correlations = np.abs(cross_correlations)
    shift = np.argmax(mag_cross_correlations) - max(len(ref),len(test))

    return shift/downsampled_rate

def shift_entry(row):
    row['error'] = ''
    try:
        row['shift'] = calculate_shift(
            os.path.join(sys.argv[1], 'converted_recordings/standard', row['filename_1']),
            os.path.join(sys.argv[1], 'converted_recordings/standard', row['filename_2']),
            row['start'],
            row['interval']
        )
    except:
        row['error'] = traceback.format_exc()

    print(row)
    return row

project.recordings['duration'] = project.recordings['filename'].map(lambda f:
    get_audio_duration(os.path.join(project.path, 'recordings', f))
)

pairs = pd.pivot_table(project.recordings, index = ['child_id', 'date_iso'], columns=project.recordings.groupby(['child_id', 'date_iso']).cumcount().add(1), values=['filename', 'duration'], aggfunc = 'first').fillna(0)
pairs.columns = pairs.columns.map('{0[0]}_{0[1]}'.format)
pairs.dropna(subset = ['filename_1', 'filename_2'], inplace = True)
pairs['min_duration'] = pairs[['duration_1', 'duration_2']].min(axis = 1)
pairs['hours'] = (((pairs['min_duration']-interval_length)/3600).astype(int)-1).apply(lambda x: max(0, x))
pairs = pairs.reindex(pairs.index.repeat(pairs.hours))
pairs['start'] = pairs.groupby(['child_id', 'date_iso']).cumcount()*3600+3600
pairs['interval'] = interval_length

pool = mp.Pool()
shifts = pool.map(shift_entry, pairs.to_dict(orient = 'recordings'))
shifts = pd.DataFrame(shifts).to_csv('output/shifts.csv')