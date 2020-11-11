import os
import pandas as pd
import sys
import multiprocessing as mp
import numpy as np
from functools import partial
import sox

from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager

project = ChildProject(sys.argv[1])
project.read()

# compute the minimum audio duration for each pair of recordings
def get_audio_duration(filename):
    if not os.path.exists(filename):
        return 0

    duration = 0
    try:
        duration = sox.file_info.duration(filename)
    except:
        pass

    return duration

project.recordings['duration'] = project.recordings['filename'].map(lambda f:
    get_audio_duration(os.path.join(project.path, 'recordings', f))
)

min_durations = project.recordings.groupby(['child_id', 'date_iso'])['duration'].min().reset_index().rename(columns = {'duration': 'min_duration'})
recordings = project.recordings.merge(min_durations, left_on = ['child_id', 'date_iso'], right_on = ['child_id', 'date_iso'])

# compute derived metrics for every vtc annotation
am = AnnotationManager(project)
am.annotations = am.annotations.merge(recordings[['filename', 'min_duration', 'duration']], left_on = 'recording_filename', right_on = 'filename')

vtc = am.annotations[am.annotations['set'] == 'vtc']
vtc = vtc[vtc['error'].isnull()]

def get_stats(am, af):
    try:
        annotation = am.annotations[am.annotations['annotation_filename'] == af]
        segments = am.get_segments(annotation)
        segments = am.clip_segments(segments, 0, segments['min_duration'].min())
        print(af, segments.shape[0])
        df = am.get_vc_stats(segments).reset_index().assign(annotation_filename = af)
    except:
        df = pd.DataFrame()
    
    return df

if not os.path.exists('output/all_stats.csv'):
    pool = mp.Pool()
    all_stats = pool.map(
        partial(get_stats, am),
        vtc['annotation_filename'].tolist()
    )

    all_stats = pd.concat(all_stats)
    all_stats = all_stats.merge(vtc[['annotation_filename', 'recording_filename']], how = 'left', left_on = 'annotation_filename', right_on = 'annotation_filename')
    all_stats = all_stats.merge(recordings[['filename', 'child_id', 'date_iso', 'min_duration']], how = 'left', left_on = 'recording_filename', right_on = 'filename')
    all_stats.to_csv('output/all_stats.csv', index = False)

all_stats = pd.read_csv('output/all_stats.csv')