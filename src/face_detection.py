import face_recognition
import cv2 as cv
import numpy as np
import os
from glob import glob
from datetime import date, datetime

#local
import config


#add the registered faces and encodings
def get_registered_faces_info():
    DIR = f'{config.REGISTERED_IMAGES}/*'
    folder_names = glob(DIR)
    
    known_face_encodings = []
    known_face_names = []

    for folder_name in folder_names:
        name = folder_name.split("/")[-1]
        image_names = glob(folder_name+"/*.jpg")
        for image_name in image_names:
            image = face_recognition.load_image_file(image_name)
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name.capitalize())

    return known_face_encodings, known_face_names




#save frame to the location
def save_frame(frame):
    today = date.today()
    today_path = f'{config.DETECTION_LOGS}/{today}'

    if not os.path.exists(today_path):
        os.makedirs(today_path)

    file_name = f"{today_path}/intruder_{datetime.now()}.jpg"
    cv.imwrite(file_name,frame)

def recognize_face(known_face_encodings,known_face_names,frame):
    small_frame = cv.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame, 3)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


    face_names = []
    #detect faces and add to face_names
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == 'Unknown':
            color = (0,0,255)
        else:
            color = (0,255,0)

        cv.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv.FILLED)

        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    
    if 'Unknown' in face_names:
        save_frame(frame)

    return frame
    
