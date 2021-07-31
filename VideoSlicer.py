from skimage import io
import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

'''
VideoSlicer:

Class that uses cv2 to slice videos

USAGE:

vid_slicer = VideoSlicer(color='red') # your options are 'red' 'green' 'blue'
list_of_vids = vid_slicer.slice_video(video = 'video.mp4')

'''
class VideoSlicer:

  def __init__(self, color):
    self.color = color
  '''
  slice_video method splits up each ASL video according to whether or not the test subject is signing or not. The goal of this method is to split up the input video of 7 signs into 7 individual short videos. 
   
  PARAMS:
    - video: a 50-60 second video of 7 signs of a single word
  
  OUTPUT:
    - a list of the names of the 7 individual videos. Each of these videos corresponds to a single instance of a sign.

  '''
  def slice_video(self,video):
    cap = cv2.VideoCapture(video) # open the video as a cv2 video object
        # Initiate holistic model
    fps = cap.get(cv2.CAP_PROP_FPS)  # get the frames per second
    
    times = [] # list of all the times 
    reds = [] # list of all the color percentages 
    while cap.isOpened(): # open the video
      ret, frame = cap.read() # read in a frame 
      current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES) # get the number current frame, i.e. this is frame 2 
      # Recolor Feed
      if frame is None: # no more frames, break out 
        break # break
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB
      image = image[350:750,100:350] # crop image to just fit the light
      # Make Detections
      
      num_red = self._picture_to_arr(image) # count the number of red pixels 
      times.append(current_frame/fps) # calculate the time 
      reds.append(num_red) # add to list 
      print(f'Number of red pixels {num_red}')
      print(f'Current second {current_frame/fps}')
    cap.release()
    cv2.destroyAllWindows()
    video_names = []
    time_tuples = [] # list of time tuples containing (start_index, stop_index)

    # iterate through the reds 
    for idx, ele in enumerate(reds):
      if ele < 30 and reds[idx-1]>30: # change start index
        start_index = idx
      if ele > 30 and reds[idx-1]<30: # change stop indexs 
        stop_index = idx
        time_tuples.append((start_index,stop_index))
    
    for start_index, stop_index in time_tuples:
      start_time = times[start_index]
      end_time = times[stop_index]
      
      name_of_video = video.replace(".mp4","")+"_"+str(int(start_time))+"s_to_"+str(int(end_time))+"s.mp4"
      video_names.append(name_of_video)

      # Write to video 
      ffmpeg_extract_subclip(video, start_time, end_time, targetname=name_of_video)
    return video_names

  '''
  _picture_to_arr 
  
  PURPOSE: The purpose of this methodis to calculate the total %tage of RGB values in an image

  PARAMS: 
    - image: the input image (ideally small so the model runs fast)

  OUTPUT:
    - floating point value that represents the percentage of red,green, and blue in an image
  
  '''
  def _picture_to_arr(self, image):
      arr = image
      arr_list=arr.tolist()
      r=g=b=0
      for row in arr_list:
          for item in row:
              r=r+item[0]
              g=g+item[1]
              b=b+item[2]  
      total=r+g+b
      red=r/total*100
      green=g/total*100
      blue=b/total*100
      #print(f'Green: {green}, Red: {red}, Blue: {blue}')
      if self.color == 'red':
        return red
      if self.color == 'green':
        return green
      return blue





   



        


