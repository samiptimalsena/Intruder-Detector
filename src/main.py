import os
from config import REGISTERED_IMAGES,DETECTION_LOGS
import cv2 as cv


#local
from face_detection import (
    get_registered_faces_info,
    recognize_face,
)
if not os.path.exists(DETECTION_LOGS):
    os.makedirs(DETECTION_LOGS)

#setup
video_capture = cv.VideoCapture(0)

#get saved infos
known_face_encodings, known_face_names = get_registered_faces_info()


while True:
    _, frame = video_capture.read()
    
    frame_inference = recognize_face(
        known_face_encodings,
        known_face_names,
        frame
    )
    

    cv.imshow('Video', frame_inference)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()
