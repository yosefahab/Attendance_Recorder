import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime, date

# database path
path = "Database_Images"

# list of images and names
database_images = []
known_face_names = []

# list names of images in path specified
imageNames = os.listdir(path)

for img in imageNames:
    currentImg = cv2.imread(f'{path}/{img}')
    # load images
    database_images.append(currentImg)
    # extract names for images
    known_face_names.append(os.path.splitext(img)[0])


#if no images in database, terminate
if not database_images:
    exit("Error: Empty Database!")

# create file for today
AttendanceFile = "Attendances/{}.csv".format(date.today().strftime("%d-%m-%Y"))
if not os.path.isfile(AttendanceFile):
    open(AttendanceFile, 'w').close()


def recordAttendance(name):
    with open(AttendanceFile, 'r+') as file:
        records = file.readlines()
        nameList = []
        for line in records:
            entry = line.split(',')
            #entry[0] is name
            nameList.append(entry[0])
        if name not in nameList:
            time = datetime.now().strftime('%H:%M')
            file.writelines(f'\n{name},{time}')


# generate encodings from given list of images
def generateEncodings(database_images):
    encodedList = []
    for img in database_images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        unknown_encoding = face_recognition.face_encodings(img)
        #some images might fail to be encoded
        if len(unknown_encoding):
            encodedList.append(unknown_encoding[0])
        else:
            print("couldnt encode: " + img)
    return encodedList


knownEncodedList = generateEncodings(database_images)
print("Encoding complete")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
process_this_frame = True
while True:
    success, frame = video_capture.read()

    # for optimisation, each frame is resized to 1/4 of its value
    resizedFrame = cv2.resize(frame, (0, 0), None, fx=0.25, fy=0.25)
    
    if process_this_frame:
        currFacesLocations = face_recognition.face_locations(resizedFrame)
        currFacesEncodings = face_recognition.face_encodings(resizedFrame, currFacesLocations)
        
        for encoding, location in zip(currFacesEncodings, currFacesLocations):
            # matches is a list containing true or false values for each image
            # for improved accuracy, a tolerance of 0.5 is used --subject to change...
            matches = face_recognition.compare_faces(
                knownEncodedList, encoding, 0.5)
            faceDistance = face_recognition.face_distance(knownEncodedList, encoding)
            matchIndex = np.argmin(faceDistance)
            name = 'Unknown'
            if matches[matchIndex]:
                name = known_face_names[matchIndex].upper()
                recordAttendance(name)
            y1, x1, y2, x2 = location
            y1, x1, y2, x2 = y1*4, x1*4, y2*4, x2*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x2, y2),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

        cv2.imshow('Video', frame)

    process_this_frame = not process_this_frame

        # waitKey(1) wait 1ms for keypress then return decimal value of pressed key (113 in the case of 'q')
        # which is then converted to binary 01110001
        # & masks it with hexadecimal value of 'FF' (11111111)
        # finally check if it matches 113 then q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        break

cv2.destroyAllWindows()
