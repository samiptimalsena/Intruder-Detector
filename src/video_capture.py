import cv2 as cv
import streamlit as st
import os
import numpy as np
import config
from face_detection import get_registered_faces_info,recognize_face

def startcam(FRAME_WINDOW):
    known_face_encodings, known_face_names = get_registered_faces_info()
    video_capture = cv.VideoCapture(0)

    while True:
        _, frame = video_capture.read()
        frame_inference = recognize_face(known_face_encodings,known_face_names,frame)
        frame_inference = cv.cvtColor(frame_inference,cv.COLOR_BGR2RGB)

        FRAME_WINDOW.image(frame_inference)

def collect_data(FRAME_WINDOW, user):

    video_capture = cv.VideoCapture(0)

    count=0
    image_added = 1

    while True:
        _, frame = video_capture.read()
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        if count > 50:
            break

        FRAME_WINDOW.image(rgb_frame)

        if count % 10 == 0 and count<=50:
            print(f"{image_added}  image added")
            path = config.REGISTERED_IMAGES+"/"+user+"/image"+str(count)+".jpg"
            cv.imwrite(path,cv.cvtColor(rgb_frame, cv.COLOR_BGR2RGB))
            image_added += 1

        count=count+1