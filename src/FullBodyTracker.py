#!/usr/bin/env python
# coding: utf-8
import mediapipe as mp
import cv2


'''
FullBodyTracker: A class used to output the coordinates of hands, head, and posture given a input video stream.

USAGE:

tracker = FullBodyTracker(show_hands=True, show_face=True,show_pose = False)

# To Track:
minimum_detection_confidence = 0.5 # Hyperparameters 
minimum_tracking_confidence = 0.5 
  
tracker.track(video=0, minimum_d_confidence=minimum_detection_confidence, minimum_t_confidence=minimum_tracking_confidence)

'''
class FullBodyTracker:

    '''
    FullBodyTracker class has 1 main utility --> track and identify the position of an individual's hands, face, and posture.

    The constructor takes in 3 boolean parameters (show_hands, show_face, show_pose), all of which display the ground truth labels on the image.
    '''
    def __init__(self, show_hands, show_face, show_pose):
        self.show_hands = show_hands
        self.show_face = show_face
        self.show_pose = show_pose

    '''
    The track method takes in the url of the video or the video object itself and detects the x,y,z positions of the hands, face, and pose.

    PARAMETERS:
        - video: the video object or a url to said video
        - minimum_d_confidence: the minimum detection confidence for the detection model
        - minimum_t_confidence: the minimum tracking confidence for the tracking model
    '''
    def track(self, video, minimum_d_confidence, minimum_t_confidence):
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic


        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)


        cap = cv2.VideoCapture(video)
        # Initiate holistic model
        with mp_holistic.Holistic(min_detection_confidence=minimum_d_confidence, min_tracking_confidence=minimum_t_confidence) as holistic:
            
            while cap.isOpened():
                ret, frame = cap.read()
                
                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Make Detections
                results = holistic.process(image)
                # print(results.face_landmarks)
                
                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                
                # Recolor image back to BGR for rendering
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image_width = image.shape[1]
                image_height = image.shape[0]
                
                # 1. Draw face landmarks
                if self.show_face:
                    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                            mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                            )
                
                # 2. Right hand
                if self.show_hands:
                    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                            )

                    # 3. Left Hand
                    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                            )

                # 4. Pose Detections
                if self.show_pose:
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                            )
                if results.pose_landmarks:   
                    print(f'Nose coordinates: ('f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, 'f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
                    print(f'Nose coordinates: ('f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, 'f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
      )
                if self.show_pose or self.show_face or self.show_hands:
                    cv2.imshow('Raw Webcam Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

#results.right_hand_landmarks
#results.left_hand_landmarks
#results.pose_landmarks






