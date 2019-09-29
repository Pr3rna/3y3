from sys import argv
import sys
import face_recognition
import cv2
import numpy as np
import time
import pickle

args = argv[1:]

if(len(args) == 0):
    sys.exit(12)

user_name = args[0]


fpsLimit = 1  # throttle limit
startTime = time.time()
video_capture = cv2.VideoCapture(0)

# "known" folder consist preprocessed encodings and names
with open("/lib/security/third_eye/known/known_encodings.txt", "rb") as fp:
    known_face_encodings = pickle.load(fp)

with open("/lib/security/third_eye/known/known_names.txt", "rb") as fp:
    known_face_names = pickle.load(fp)

print(known_face_names)
if user_name not in known_face_names:
    print("user name not present")
    sys.exit(12)

user_face_encoding = known_face_encodings[known_face_names.index(
    user_name)]  # user

face_locations = []
face_encodings = []
face_names = []
count = 0
flag = 0

while True:
    # Grab a single frame of video
    try:
        nowTime = time.time()
        if (int(nowTime - startTime)) > fpsLimit:
            ret, frame = video_capture.read()
            count = count + 1
            if count > 3:                # Time exceeded
                video_capture.release()
                cv2.destroyAllWindows()
                print("timeout")
                sys.exit(12)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(
                rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    [user_face_encoding], face_encoding)

                if True in matches:
                    video_capture.release()
                    cv2.destroyAllWindows()
                    flag = 1
                    print("foud user")
                    sys.exit(0)  # user found

            startTime = time.time()

        # cv2.imshow('Video', frame)

    except:
        print("reached here", flag)
        if flag == 1:
            sys.exit(0)
        if count > 3:
            video_capture.release()
            cv2.destroyAllWindows()
            sys.exit(12)
