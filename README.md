# Face_Recognition
This project aims to capture attendance using the opencv library.

# Setup 
To download OpenCV on windows you need to have python installed.
then run:
```
pip3 install opencv-python
```

To download OpenCV on raspberryPi a simple tutorial can be found here: [Tutorial](https://tutorials-raspberrypi.com/installing-opencv-on-the-raspberry-pi/)

# Directories 
- /Scripts contains bash script to automate capturing of images for database which is later used to record the attendance.
- /Database_images contains all images used by the system.
- /Attendances contains .csv files containing recorded attendances.

# Scripts
- the /Scripts directory contains a bash script to automate the capturing of images.
- currently there's only a script for linux only.
- note that this script only works with bash.
- this script requires that you have fswebcam installed, to install fswebcam run:
```
sudo apt install fswebcam
```

# Process 
System works in the following manner:
1. Images are loaded from the database(/Database_images) and names are extracted from the images' names, thus each image must be named after the person pictured.
2. if a file with current date isnt present in /Attendances then a new .csv file is created.
3. A list is created containing all encodings of known images.
4. for optimisation sake, each frame is resized to 1/4 of its value, and only process every other frame.
5. faces are captured from frames, encodings are then generated from those faces and compared to existing faces.

# About Pi
Compatability with raspberry pi will be added soon, such as support for raspberry pi camera.


**Project is still in development and more features will be added soon**
**Feel free to contribute!**
