import face_recognition
import cv2
import numpy as np
import time
import pickle
import sys

def exi(name):
    a = open('./test.txt', 'w')
    a.write(name)
    a.close()


fpsLimit = 1  # throttle limit
startTime = time.time()
video_capture = cv2.VideoCapture(0)

# "known" folder consist preprocessed encodings and names
with open( "./known/known_encodings.txt", "rb") as fp:
    known_face_encodings = pickle.load(fp)

with open("./known/known_names.txt", "rb") as fp:
    known_face_names = pickle.load(fp)

face_locations = []
face_encodings = []
face_names = []
count = 0

running = True
while running:
    # Grab a single frame of video
    try:
        nowTime = time.time()
        if (int(nowTime - startTime)) > fpsLimit:
            ret, frame = video_capture.read()
            count = count + 1
            print(count)
            if count > 3:
                video_capture.release()
                cv2.destroyAllWindows()
                exi("unknown")
                running=False
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(
                rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                
                if True in matches:
                    print("got a true value")
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # If found then exit
                    video_capture.release()
                    cv2.destroyAllWindows()
                    print("name of the person", name) 
                    exi(name)  # person detected
                    running=False
                    
                else:
                    video_capture.release()
                    cv2.destroyAllWindows()
                    exi("guest")
                    running=False
            startTime = time.time()

        #cv2.imshow('Video', frame)

    except:
        if count > 3:
            video_capture.release()
            cv2.destroyAllWindows()
            print("Terminate!")
            exi("unknown")  # person not detected
            running=False
            
