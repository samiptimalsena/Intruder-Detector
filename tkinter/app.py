# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog

import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
import numpy as np
import os
from tkinter import simpledialog
from datetime import datetime

# Structure and Layout
window = Tk()
window.bind('<Escape>', lambda e: window.quit())


window.title("Unauthorized personnel Detector")
window.geometry("590x700")
# window.config(background='yellow')

style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='wn')


cap = cv2.VideoCapture(0)

# Functions


# Read face data
# Face Detection

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

def handle_username_input():
   username = simpledialog.askstring("Input", "What is your first name?", parent=window)
   read_face_data(username)

def read_face_data(username):
   start_time = datetime.now()
   print(start_time)
   # os.system(f'python3 read_face_data.py {username}')
   ret,frame = cap.read()
   face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
   skip = 0
   face_data = []
   while True:
      ret,frame = cap.read()
      if ret:
         faces = face_cascade.detectMultiScale(frame, 1.3, 5)
         faces = sorted(faces, key = lambda f:f[2]*f[3])

         face_section = np.zeros((100,100,3))

         # Pick the last face (coz it is largest face)
         for face in faces[-1:]:
            x,y,w,h = face
            cv2.rectangle(frame, (x,y), (x+w, y+h),(255,0,0),2)

            # Crop out required face
            offset = 10 # padding 10px for cropped image
            face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
            face_section = cv2.resize(face_section, (100,100))

            # Store 10 face
            skip += 1
            if skip%10==0:
               face_data.append(face_section)
               print(len(face_data))

            cv2.imshow("Video Frame",frame)
            cv2.imshow("Face Section",face_section)

      key_pressed = cv2.waitKey(1) & 0xFF
      if key_pressed == ord('q'):
         cv2.destroyAllWindows()
         break



   face_data = np.asarray(face_data)
   face_data = face_data.reshape((face_data.shape[0], -1))

   np.save('./data/'+username+'.npy',face_data)
   print("Data successfullt saved at "+'./data/'+username+'.npy')


def start_service():
      ########### KNN algo ###########
   def distance(v1, v2):
      # Eucledian
      return np.sqrt(((v1-v2)**2).sum())

   def knn(train, test, k=5):
      dist = []

      for i in range(train.shape[0]):
         # Get the vector and label
         ix = train[i, :-1]
         iy = train[i, -1]
         # Compute the distance from test point
         d = distance(test, ix)
         dist.append([d, iy])
      # Sort based on distance and get top k
      dk = sorted(dist, key=lambda x:x[0])[:k]
      # Retrieve only the labels
      labels = np.array(dk)[:, -1]

      # Get frequencies of each label
      output = np.unique(labels, return_counts=True)
      # Find max frequency and corresponding label
      index = np.argmax(output[1])
      return output[0][index]
   ########### KNN algo ###########

   dataset_path = './data/'

   face_data = []
   labels = []

   class_id = 0 # Labels for the given file
   names = {} # Mapping btw id - name

      # Data preparation
   for fx in os.listdir(dataset_path):
      if fx.endswith('.npy'):
         names[class_id] = fx[:-4] # santosh.npy -> santosh
         print("Loaded " + fx)
         data_item = np.load(dataset_path+fx)
         face_data.append(data_item)

         # Create Labels for the class
         target = class_id*np.ones((data_item.shape[0],))
         class_id += 1
         labels.append(target)

   face_dataset = np.concatenate(face_data, axis=0)
   face_labels = np.concatenate(labels, axis=0).reshape((-1,1))

   print(face_dataset.shape)
   print(face_labels.shape)

   # Concatinating x and y values in one matrix because knn requires one training matrix
   trainset = np.concatenate((face_dataset,face_labels),axis=1)
   print(trainset.shape)


   while True:
      ret, frame = cap.read()

      if ret == False:
         continue

      faces = face_cascade.detectMultiScale(frame, 1.3, 5)

      for (x,y,w,h) in faces:

         # Get the face ROI(Region of interest)
         offset = 10 # padding 10px for cropped image
         face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
         face_section = cv2.resize(face_section, (100,100))

         # Predicted Label (out)
         out = knn(trainset, face_section.flatten())

         # Display on the screen the name and rectangle around it
         pred_name = names[int(out)]
         cv2.putText(frame, pred_name, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
         cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,255),2)

      cv2.imshow("Faces",frame)

      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
         cv2.destroyAllWindows()
         break




# MAIN TAB
l1 = Label(window, text="Unauthorized personnel detector")
l1.grid(row=1, column=0)

# Display Screen For Result
window_display = Label(window, height=550)
window_display.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


def show_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        window_display.imgtk = imgtk
        window_display.configure(image=imgtk)
        window_display.after(10, show_frame)

show_frame()

# BUTTONS
button1 = Button(window, text="Record Your Data", command=handle_username_input,
                 width=12, bg='#e31717', fg='#fff')
button1.grid(row=4, column=0, padx=10, pady=10)

button2 = Button(window, text="Start WebCam", command=start_service,
                 width=16, bg='#2d7309', fg='#fff')
button2.grid(row=4, column=1, padx=10, pady=20)





window.mainloop()
