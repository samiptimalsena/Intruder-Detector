import os
from config import REGISTERED_IMAGES,DETECTION_LOGS
import cv2 as cv
import streamlit as st

st.title("Unauthorized personnel Detector")

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
known_face_encodings, known_face_names = get_registered_faces_info()

video_capture = cv.VideoCapture(0)
def startCam():
   while True:
      _, frame = video_capture.read()
      # frame =

      frame_inference = recognize_face(known_face_encodings,known_face_names,frame)
      frame_inference = cv.cvtColor(frame_inference,cv.COLOR_BGR2RGB)


      FRAME_WINDOW.image(frame_inference)
      #  cv.imshow('Video', frame_inference)

      if cv.waitKey(1) & 0xFF == ord('q'):
         cv.destroyAllWindows()
         break


if col2.button("Add a new user"):
   pass

if col3.button("Start Webcam"):
   startCam()

# Login system
def is_authenticated(password):
	return password == "admin"


def generate_login_block():
   block1 = st.empty()
   block2 = st.empty()

   return block1, block2

def clean_blocks(blocks):
   for block in blocks:
      block.empty()

def login(blocks):
   blocks[0].markdown("""
         <style>
               input {
                  -webkit-text-security: disc;
               }
         </style>
      """, unsafe_allow_html=True)

   return blocks[1].text_input('Password')

if col4.button("Login As Admin"):
	login_blocks = generate_login_block()
	password = login(login_blocks)
	if is_authenticated(password):
		clean_blocks(login_blocks)
	elif password:
		st.info("Please enter a valid password")

video_capture.release()
cv.destroyAllWindows()
