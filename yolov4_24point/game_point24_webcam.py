######## Game Point24 webcam #########
#
# Author: Minglai Liu
# Date: 12/06/20
# Description:
# This program uses a yolov4 trained object detector to recoginize poker cards, then calculate 24 point.
# It lperform poker cards detection on a webcam feed.
# It draws boxes and scores around the objects of interest in each frame from the webcam.
# Only 4 poker cards are detected, then the programm will print out found 24 point agrithom or not.
# If calculation is exist, print out all the formula.

## Some of the code is refered from
## https://github.com/Avnet/face_py_vart/tree/2020.1

#History:
#v4:11/21/2020  19:40: connected with 24 point calculation
#v5:11/21/2020  20:40: based on v4, v4 is OK, but will report error if no 4 cards. fix this in V5.
#V6:12/06/2020  09:35: optimize the print info

# USAGE
# python game_point24_webcam.py [--input 0] [--detthreshold 0.55] [--nmsthreshold 0.35]

import numpy as np
import argparse
import imutils
import time
import cv2
import os, errno

from imutils.video import FPS

import runner
from pokerdetect import pokerDetect
from point24 import Point24

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=False,
  help = "input camera identifier (default = 0)")
ap.add_argument("-d", "--detthreshold", required=False,
  help = "poker detector softmax threshold (default = 0.55)")
ap.add_argument("-n", "--nmsthreshold", required=False,
  help = "poker detector NMS threshold (default = 0.35)")
args = vars(ap.parse_args())

if not args.get("input",False):
  inputId = 0
else:
  inputId = int(args["input"])
print('[INFO] input camera identifier = ',inputId)

if not args.get("detthreshold",False):
  detThreshold = 0.55
else:
  detThreshold = float(args["detthreshold"])
print('[INFO] poker detector - softmax threshold = ',detThreshold)

if not args.get("nmsthreshold",False):
  nmsThreshold = 0.35
else:
  nmsThreshold = float(args["nmsthreshold"])
print('[INFO] poker detector - NMS threshold = ',nmsThreshold)

# Initialize Vitis-AI/DPU based poker detector
dpu = runner.Runner("./models/dpu_yolov4_poker")[0]
dpu_poker_detector = pokerDetect(dpu,detThreshold,nmsThreshold)
dpu_poker_detector.start()

# Initialize the camera input
print("[INFO] starting camera input ...")
cam = cv2.VideoCapture(inputId)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
if not (cam.isOpened()):
    print("[ERROR] Failed to open camera ", inputId )
    exit()

# start the FPS counter
fps = FPS().start()

# loop over the frames from the video stream
while True:
  # Capture image from camera
  ret,frame = cam.read()

  # Vitis-AI/DPU based poker detector
  pokers = dpu_poker_detector.process(frame)

  # loop over the pokers
  for i,(left,top,right,bottom) in enumerate(pokers):

    # draw a bounding box surrounding the object so we can
    # visualize it
    cv2.rectangle( frame, (left,top), (right,bottom), (0,255,0), 2)

    # convert deteced cards to real number for calculation
    data_list = []

  for item in objects:
       if item == b'ace':
           data_list.append('1')
       elif item == b'nine':
           data_list.append('9')
       elif item == b'ten':
           data_list.append('A')
       elif item == b'jack':
           data_list.append('B')
       elif item == b'queen':
           data_list.append('C')
       elif item == b'king':
           data_list.append('D')
       else: #normal number,opertion and ()
           data_list.append(item)

  print(data_list)
  
  #pass the 4 cards number to 24 point calculation programm, print out the calculation result.
  font = cv2.FONT_HERSHEY_SIMPLEX
  if len(data_list) == 4:
      str = Point24(data_list).calculate()
      str = 'I got it,24 can be calculated'
      frame = cv2.putText(frame, str, (0, 120), font, 1, (255, 0, 0), 2)

  # Display the processed image
  cv2.imshow("Poker detector and 24 Point Game", frame)
  key = cv2.waitKey(1) & 0xFF

  # Update the FPS counter
  fps.update()

  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break

# Stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] elapsed FPS: {:.2f}".format(fps.fps()))

# Stop the poker detector
dpu_poker_detector.stop()
del dpu

# Cleanup
cv2.destroyAllWindows()
