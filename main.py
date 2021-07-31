import pandas as pd
import numpy as np 

from FullBodyTracker import FullBodyTracker
from VideoSlicer import VideoSlicer

if __name__ == '__main__':
  '''
  tracker = FullBodyTracker(show_hands=True, show_face=True,show_pose=True)
  # Track
  minimum_detection_confidence = 0.5
  minimum_tracking_confidence = 0.5 
  tracker.track(video=0, minimum_d_confidence=minimum_detection_confidence, minimum_t_confidence=minimum_tracking_confidence)
  '''

  vid_slicer = VideoSlicer(color='red')
  list_of_vids = vid_slicer.slice_video(video = 'matt_test.mp4')



