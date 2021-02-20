# Core Pkg
import streamlit as st
import cv2
import os
import face_recognition
import numpy as np
from glob import glob

st.title("Unauthorized personnel Detector")

# html_page = """
# <style>
# .block-container{
#         max-width: 100%;
#     }
# </style>

# """
# html_page_2 = """
# <div style="background-color:tomato;display:flex;justify-content:space-evenly;margin:0;max-width: 100%!important;">
# 		<video width="1020" height="640" controls></video>
#       <div style="display:flex;flex-direction:column;justify-content:center;align-items:center">
#          <button style="margin:1em;padding:10px">Pass a custom video</button>
#          <button style="margin:1em;padding:10px">Pass a custom video</button>
#          <button style="margin:1em;padding:10px">Pass a custom video</button>
#       </div>
# 	</div>

# """

# st.markdown(html_page,unsafe_allow_html=True)


# st.markdown(html_page_2,unsafe_allow_html=True)

# st.title("Webcam Live Feed")
# run = st.checkbox('Run')
# FRAME_WINDOW = st.image([])
# camera = cv2.VideoCapture(0)

# while run:
#     _, frame = camera.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     FRAME_WINDOW.image(frame)
# else:
#     st.write('Stopped')


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a video file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector("/home/sant33/Downloads")
st.write('You selected `%s`' % filename)

st.write("Enter username only to add new user")
user = st.text_input("label goes here")


col1,col2,col3,col4 = st.beta_columns(4)

if col1.button("Play a video"):
   video_file = open(filename, 'rb')
   video_bytes = video_file.read()
   st.video(video_bytes)

FRAME_WINDOW = st.image([])
####################################################################################################

def recognize_user():
   known_face_encodings = list()
   known_face_names = list()

   DIR = './input/*'
   video_capture = cv2.VideoCapture(0)
   # harr_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

   folder_names = glob(DIR)

   for folder_name in folder_names:
    name = folder_name.split("/")[-1]
    image_names = glob(folder_name+"/*.jpg")
    for image_name in image_names:
        print(name)
        image = face_recognition.load_image_file(image_name)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name.capitalize())

   face_locations = list()
   face_encodings = list()
   face_names = list()
   process_this_frame = True

   while True:
    _, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)


    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame, 3)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = list()

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == 'Unknown':
            color = (0,0,255)
        else:
            color = (0,255,0)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

   #  cv2.imshow('Video', frame)
    FRAME_WINDOW.image(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
         cv2.destroyAllWindows()
         break

   # video_capture.release()
   # cv2.destroyAllWindows()

####################################################################################################################

def collect_data(user):

   os.makedirs("./input/"+user)

   video_capture = cv2.VideoCapture(0)

   if not video_capture.isOpened():
      raise Exception("Could not open video device")

   count=0
   image_added = 1
   while True:
      ret, frame = video_capture.read()
      FRAME_WINDOW.image(frame)

      if(cv2.waitKey(20) & 0XFF==ord('d')) or count >150:
         cv2.destroyAllWindows()
         break

      if count % 10 == 0:
         print(f"{image_added}  image added")
         cv2.imwrite("./input/"+user+"/image"+str(count)+".jpg",frame)
         image_added += 1

      count=count+1
      # cv2.imshow("Adding Training Data", frame)

   video_capture.release()

if col2.button("Add a new user"):
   collect_data(user)

if col3.button("Start Webcam"):
   recognize_user()

col4.button("Stop model")