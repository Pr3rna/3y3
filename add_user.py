import face_recognition
import cv2
import numpy as np
import pickle
import os
import getpass
import sys

name = sys.argv[1]
print(name)
known_face_encodings = []
known_face_names = []

if not os.path.exists("/lib/security/third_eye/known/"):
    os.makedirs(("/lib/security/third_eye/known"))

if(os.path.exists("/lib/security/third_eye/known/known_encodings.txt")):
    with open("/lib/security/third_eye/known/known_encodings.txt", "rb") as fp:
        known_face_encodings = pickle.load(fp)

if(os.path.exists("/lib/security/third_eye/known/known_names.txt")):
    with open("/lib/security/third_eye/known/known_names.txt", "rb") as fp:
        known_face_names = pickle.load(fp)


video_capture = cv2.VideoCapture(0)


while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    # press c to capture photo
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # make sure only person is in frame
        face_locations = face_recognition.face_locations(frame)
        try:
       	    face_encodings = face_recognition.face_encodings(
            frame, face_locations)[0]
        except:
            print("no face detected!")
        known_face_encodings.append(face_encodings)
        known_face_names.append(name)

        break


with open("/lib/security/third_eye/known/known_encodings.txt", "wb") as fp:
    pickle.dump(known_face_encodings, fp)

with open("/lib/security/third_eye/known/known_names.txt", "wb") as fp:
    pickle.dump(known_face_names, fp)

print("Encodings saved for user: " + name)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
