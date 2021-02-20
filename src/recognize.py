import face_recognition
import cv2 as cv
import numpy as np

video_capture = cv.VideoCapture(0)

samip_image = face_recognition.load_image_file("/home/samip/Face-Recognition-System/input/samip/samip2.jpg")
samip_face_encoding = face_recognition.face_encodings(samip_image)[0]

abishek_image = face_recognition.load_image_file('/home/samip/Face-Recognition-System/input/abishek/abishek.jpg')
abishek_face_encoding = face_recognition.face_encodings(abishek_image)[0]

santosh_image = face_recognition.load_image_file('/home/samip/Face-Recognition-System/input/santosh/santosh.jpg')
santosh_face_encoding = face_recognition.face_encodings(santosh_image)[0]

known_face_encodings = [
    samip_face_encoding,
    abishek_face_encoding,
    santosh_face_encoding
]
known_face_names = [
    "Samip",
    'Abishek',
    'Santosh'
]

face_locations = list()
face_encodings = list()
face_names = list()
process_this_frame = True

while True:
    _, frame = video_capture.read()

    small_frame = cv.resize(frame, (0,0), fx=0.25, fy=0.25)

    rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
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

        cv.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv.FILLED)

        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()