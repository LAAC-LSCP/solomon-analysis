import os
import pandas as pd
import sys

from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager, Segment

from pyannote.core import Timeline, Annotation, Segment
from pyannote.core.notebook import Notebook
import pyannote.metrics.diarization as diarization
import pyannote.metrics.identification as identification
import pyannote.metrics.detection as detection

from matplotlib import pyplot as plt

def segments_to_pyannote(segments, column = 'speaker_type', ignore = []):
    annotation = Annotation()
    
    for segment in segments.to_dict(orient = 'records'):
        if segment[column] in ignore:
            continue

        start = segment['segment_onset'] + segment['time_seek']
        end = segment['segment_offset'] + segment['time_seek']

        annotation[Segment(start, end)] = segment[column]

    return annotation

set_a, set_b = sys.argv[2], sys.argv[3]
project = ChildProject(sys.argv[1])
am = AnnotationManager(project)

a = am.annotations[am.annotations['set'] == set_a]
b = am.annotations[am.annotations['set'] == set_b]

a.loc[a.range_offset == 0, 'range_offset'] = 100000
b.loc[b.range_offset == 0, 'range_offset'] = 100000

a, b = am.intersection(a, b)

a = a.to_dict(orient = 'records')
b = b.to_dict(orient = 'records')

for left, right in zip(a, b):
    left_segments = am.get_segments(pd.DataFrame([left]))
    right_segments = am.get_segments(pd.DataFrame([right]))

    if left_segments.shape[0] == 0 or right_segments.shape[0] == 0:
        continue
    
    left_segments = am.clip_segments(left_segments, left_segments['range_onset'], left_segments['range_offset'])
    right_segments = am.clip_segments(right_segments, right_segments['range_onset'], right_segments['range_offset'])

    metric = identification.IdentificationErrorRate(parallel = True)
    ref = segments_to_pyannote(left_segments, ignore = ['SPEECH'])
    hyp = segments_to_pyannote(right_segments, ignore = ['SPEECH'])

    value = metric(ref, hyp, detailed = True)
    print(value)

    plt.clf()
    notebook = Notebook()
    plt.rcParams['figure.figsize'] = (notebook.width, 10)

    # Plot reference
    plt.subplot(211)
    notebook.plot_annotation(ref, legend=True, time=False)
    plt.gca().set_title('reference', fontdict={'fontsize':18})

    # Plot hypothesis
    plt.subplot(212)
    notebook.plot_annotation(hyp, legend=True, time=True)
    plt.gca().set_title('hypothesis', fontdict={'fontsize':18})
    plt.show()
