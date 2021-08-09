# This is a prorotype for a code that works on raspberry pi

import face_recognition
import cv2
import numpy as np
import os
from datetime import date,datetime
# some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.
filename = '/home/pi/mu_code/Face_Recognition/Attendance/{}.txt'.format(date.today().strftime("%d-%m-%Y"))
try:
    attendance = open(filename,"r+")
except:
    attendance = open(filename,"w")
    attendance.write('{0:<10} {1:>16}'.format("Name","Recorded at")+'\n')
    attendance.close()
    attendance = open(filename,"r+")
def addName(name):
    names = attendance.readlines()
    for line in names:
        if name in line:
            print("found name:"+name)
            return
    else:
        attendance.write('{0:<10} {1:>16}'.format(name,str(datetime.now().strftime("%H:%M:%S")))+ '\n')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Create arrays of known face encodings and their names
face_encoding_array=[]
known_face_names = []
known_face_encodings =[]
directory = '/home/pi/mu_code/Face_Recognition/Database_images'
for index,filename in enumerate(os.listdir(directory)):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Load a sample picture and learn how to recognize it.
        unknown_image = face_recognition.load_image_file(os.path.join(directory, filename))
        unknown_encoding = face_recognition.face_encodings(unknown_image)
        if len(unknown_encoding):
            known_face_encodings.append(unknown_encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])
        else:
            print(filename + " Could not be encoded")
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    #ret checks if frame is captured
    ret, frame = video_capture.read()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        #empty list before adding new names
        face_names.clear()
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.55)
            name = "Unknown"
            #use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if name != 'Unknown':
                tempname = "".join(filter(lambda x: not x.isdigit(),name))
                addName(tempname)
                face_names.append(tempname)
            else:
                face_names.append(name)
    process_this_frame = not process_this_frame

    #Display the results
    #face_locations: coordinates of frame, face_names: each face's name processed in frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with a name below the face                   BGR
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    #waitkey: pause and display frame for ms
    if cv2.waitKey(1) & 0xFF== ord('q'): #optional 
        break

attendance.close()
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()