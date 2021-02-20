import os
from config import REGISTERED_IMAGES,DETECTION_LOGS
import cv2 as cv
import numpy as np
import streamlit as st
from datetime import date
from glob import glob


st.title("Intruder Detector")

# st.write("Enter username only to add new user")
user = st.text_input("label goes here")

col1,col2,col3,col4 = st.beta_columns(4)


FRAME_WINDOW = st.image([])

#local
from face_detection import (
    get_registered_faces_info,
    recognize_face,
)
if not os.path.exists(DETECTION_LOGS):
    os.makedirs(DETECTION_LOGS)

#setup


#get saved infos
known_face_encodings, known_face_names = [None,None]

video_capture = None
def startCam():
   known_face_encodings, known_face_names = get_registered_faces_info()
   video_capture = cv.VideoCapture(0)
   while True:

      _, frame = video_capture.read()
      # frame =

      frame_inference = recognize_face(known_face_encodings,known_face_names,frame)
      frame_inference = cv.cvtColor(frame_inference,cv.COLOR_BGR2RGB)


      FRAME_WINDOW.image(frame_inference)
      #  cv.imshow('Video', frame_inference)

      if cv.waitKey(1) & 0xFF == ord('q'):
         video_capture.release()
         cv.destroyAllWindows()
         break


def collect_date(user):
   os.makedirs("../input/"+user)

   video_capture = cv.VideoCapture(0)

   if not video_capture.isOpened():
      raise Exception("Could not open video device")

   count=0
   image_added = 1
   while True:
      ret, frame = video_capture.read()
      frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        
      #add completed message img
      if count > 150:
         frame = np.zeros((500,500,3), dtype='uint8')
         frame[:] = 255
         cv.putText(frame, "Completed ", (200, 300), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
        
      FRAME_WINDOW.image(frame)  
        
      if(cv.waitKey(20) & 0XFF==ord('d')) or count >150:
         cv.destroyAllWindows()
         break

      if count % 10 == 0:
         print(f"{image_added}  image added")
         cv.imwrite("../input/"+user+"/image"+str(count)+".jpg",frame)
         image_added += 1

      count=count+1
      # cv.imshow("Adding Training Data", frame)

   video_capture.release()

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images



if col2.button("Add a new user"):
   video_capture = None
   collect_date(user)



def get_intruders():
   folder_path = f"../detection_logs/{date.today()}/*"
   file_names = glob(folder_path)[:5]
   images_frames = []

   images_frames = st.beta_columns(5)

   for i, file_path in enumerate(file_names):
      img = cv.imread(file_path)
      img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
      images_frames[i].image(img,width=200)



if col3.button("Start Webcam"):
   startCam()


if col4.button("Admin Panel"):
   get_intruders()

# video_capture.release()
cv.destroyAllWindows()
