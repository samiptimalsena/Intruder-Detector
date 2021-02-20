import cv2 as cv
import os


user=input("Enter the name of the person \n")

while os.path.exists("/home/samip/Face-Recognition-System/input/"+user):
    print('User with this name already exist. Please try again with new name or press ctrl+c to quit')
    user=input("Enter the name of the person \n")

os.makedirs("/home/samip/Face-Recognition-System/input/"+user)

video_capture = cv.VideoCapture(0)

if not video_capture.isOpened():
    raise Exception("Could not open video device")

count=0
image_added = 1
while True:
    ret, frame = video_capture.read()

    if(cv.waitKey(20) & 0XFF==ord('d')) or count >150:
        break

    if count % 10 == 0:
        print(f"{image_added}  image added")
        cv.imwrite("/home/samip/Face-Recognition-System/input/"+user+"/image"+str(count)+".jpg",frame)
        image_added += 1

    count=count+1
    cv.imshow("Adding Training Data", frame)

video_capture.release()