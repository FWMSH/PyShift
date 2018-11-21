#!/usr/bin/env python3

import sys
import freenect
import cv2
import numpy as np
import time
from os.path import isfile

# =====================DEFAULTS=====================
# these will scale the images
#   <1 : better performance, but worse picture quality
#   =1 : no scale
#   >1 : image scaled up (degrades performance, only use if you know what you're doing)
X_SCALE = 1 # width multiplier 
Y_SCALE = 1 # height multiplier
FRAMES_TO_MEAN = 4 # ammount of frames to mean to "smooth"
IMAGE_FILE = "input.jpg"

# Flash Fix Settings
FLASH_FIX = False # Fixes rare cases of flashing
MAX = 15 # max ammount we will let smoothed get to
MIN = -15 # min ammount we will let smoothed get to

DEBUG = False # enables debug output

# =====================OPTIONS=====================
if len(sys.argv) > 1:
    print("setting image to " + sys.argv[1])
    IMAGE_FILE = sys.argv[1]
    
# check if file exists
if not isfile(IMAGE_FILE):
    print(IMAGE_FILE + " was not found!!!")
    sys.exit(1)

# setup window
cv2.namedWindow("Depth", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Depth",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
keep_running = True

# Get image
base_img = cv2.imread(IMAGE_FILE, cv2.IMREAD_COLOR)

# make sure cv2 recognized the image
if base_img is None:
    print(IMAGE_FILE + " not recognized, please use an image")
    sys.exit(2)

# scale image
base_img = cv2.resize(base_img, (0,0), fx=X_SCALE, fy=Y_SCALE)
HEIGHT, WIDTH, ch = base_img.shape

# split image into base color channels
blue_img, green_img, red_img = cv2.split(base_img)

depth_log = list()
diff_log = list()
mean_log = list()

# img_merg(vr)
#   ARGS: 
#       vr - float of the 'smoothed' scale used to determine the intensity of each color
#   RETRNS:
#    cv2 image for your frame
def img_merg(vr):
    # These are two knobs to fiddle the slope of the change
    parm1 = 0.8
    parm2 = 0.8
    
    parm3 = 1 - parm2
    
    R = (parm2 + (parm3 * (vr)))*(1/parm1)
    G = (parm1 + (parm1 * (1.0 - abs(vr)))) / 2
    B = (parm2 + (parm3 * (-1.0 * vr)))*(1/parm2)
    
    if DEBUG:
        print(R,G,B)
    
    im = cv2.merge((cv2.multiply(blue_img, B), cv2.multiply(green_img, G), cv2.multiply(red_img, R)))
    return im

# display_depth(dev, data, timestamp)
#   ARGS:
#       dev - kinect device handle
#       data - depth data from our kinect depth sensor
#       timestamp - timestamp of the image
#   INFO:
#       This method is called everytime the kinect returns a depth-frame.
def display_depth(dev, data, timestamp):
    global keep_running
    global depth_log
    global diff_log
    global mean_log
    global MAX
    global MIN
    global DEBUG
    
    # add our depth data to our log
    depth_log.append(np.percentile(data,10))
    
    # get the difference between current & last
    if len(depth_log) > 1 and depth_log[-1] and depth_log[-2]:
        difference = depth_log[-1] - depth_log[-2]
    else:
        if DEBUG:
            print("[DEPTH] Skipping diff")
        difference = 0 # our default for rare edge cases (startup, etc.)
        
    diff_log.append(difference)
    
    if len(diff_log) >= FRAMES_TO_MEAN:
        mean_log.append(np.mean(diff_log[-FRAMES_TO_MEAN:-1]))
    else:  
        mean_log.append(0)
    
    # FLASH FIX
    #   if the mean is not close to the last mean, throw the frame out and use the previous mean (data was invalid)
    #   
    #   (good for low frame rates)
    if len(mean_log) > 1 and mean_log[-1] and mean_log[-2] and FLASH_FIX:
        if (mean_log[-1] < 0 and mean_log[-2] < 0) or (mean_log[-1] > 0 and mean_log[-2] > 0): # make sure they are the same direction
            if (mean_log[-1] - mean_log[-2] > MAX) or (mean_log[-1] - mean_log[-2] < MIN): # check limits
                mean_log[-1] = mean_log[-2] # revert to previous frame
                if DEBUG:
                    print("caught flash")
        else:
            mean_log[-1] = 0 # should give us a 'null' effect when we are in-between directions
    elif DEBUG:
        print("[DEPTH] Skipping Flash Fix")
                    
    smoothed = mean_log[-1]
    
    if DEBUG:
        print("[DEPTH] Smoothed: " + str(smoothed))
    
    # call img_merg with lower intensity
    im = img_merg(smoothed/5)

    cv2.imshow('Depth', im)
    if cv2.waitKey(1) == 27:
        keep_running = False

def body(*args):
    if not keep_running:
        raise freenect.Kill

# start freenect loop
print('Press ESC in window to stop')
freenect.runloop(depth=display_depth,
                 body=body)
