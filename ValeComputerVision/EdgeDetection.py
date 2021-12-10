#!/usr/bin/env python3
# Import Libraries. 
# Make sure to install on your device all the following libraries first.

import cv2
import depthai as dai
import numpy as np
import time
import pixellib
from pixellib.semantic import semantic_segmentation
import time

# Load Segmentation Model
segment_frame = semantic_segmentation()
segment_frame.load_ade20k_model("deeplabv3_xception65_ade20k.h5")

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

# name the display window
xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(300,300)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.preview.link(xoutRgb.input)

# masking color array boundaries
# lowerBlue = np.array([245,0,0])
# upperBlue = np.array([255,10,3])

# kernel = np.ones((2,2), np.uint8)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    print('Connected cameras: ', device.getConnectedCameras())
    # Print out usb speed
    print('Usb speed: ', device.getUsbSpeed().name)

    # Output queue will be used to get the rgb frames from the output defined above
    queue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:

        # blocking call, will wait until a new data has arrive
        frame = queue.get()  

        # Convert frame to cv2 format
        imgOut = frame.getCvFrame()

        # Save Image Frame
        cv2.imwrite('imOut.jpg', imgOut)

        # Start segmentation time
        startSegTime = time.time()

        # Apply the segmentation model and save new image frame
        segment_frame.segmentAsAde20k("imOut.jpg", output_image_name = "imgOut.jpg", overlay=False)

        # stop segmentation time
        endSegTime = time.time()
        print(f"Runtime of segmentation is:{endSegTime - startSegTime}")

        # start Image Filtering time
        startFiltTime = time.time()

        # Read the new segmented image frame
        segImg = cv2.imread('imgOut.jpg')

        # Do image filtering after segmentation is applied
        # blueMask = cv2.inRange(segImg,lowerBlue, upperBlue)

        # result = cv2.bitwise_and(segImg,segImg,blueMask,blueMask)

        # Apply canny edge detector
        edges = cv2.Canny(segImg,100,200)
        edgesOut = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Create a copy of applied edges frame mask
        copEdges = np.copy(edgesOut)

        # Apply Probabilistic Hough Line Transform
        linesP = cv2.HoughLinesP(image = edges, rho = 1, theta = np.pi / 180 , threshold = 100, lines = None, minLineLength = 40, maxLineGap = 10)

        # Create variable for detected hough line angles
        angle = 0

        # Draw the lines
        if linesP is not None:
             for i in range(0, len(linesP)):
                 l = linesP[i][0]
                 x1 = l[0]
                 y1 = l[1]
                 x2 = l[2]
                 y2 = l[3]
                 angle = np.arctan2((y1 - y2),(x1 - x2))

                 # Omit horizontal hough lines from being detected
                 if (-3.00 < angle < 3.00):
                    cv2.line(copEdges, pt1 = (l[0], l[1]), pt2 = (l[2], l[3]), color = (0,0,255), thickness = 2, lineType = cv2.LINE_AA)
                    # print("Angle:",angle)

        # Angle print statement for testing
        # print(angle)

        # Integer variables for pixel count of probe lines and hough line intersection
        count1 = 0
        count2 = 0

        # Pixel count position of where first hough line pixel intersection is detected
        redpos1 = 0
        redpos2 = 0

        # Create a copy of edges mask with detected hough lines
        compvis = np.copy(copEdges)
        
        # loop through each probe line pixel of line 1 and line 2 on 300 x 300 image frame
        # Both lines are vertical with a y range from 230 to 300 of image
        # Origin (0,0) of image frame starts from top left corner
        for imgy in range(230,300):

            # BRG color values from specific pixel of each line
            b1, g1, r1 = compvis[imgy,200]
            b2, g2, r2 = compvis[imgy,100]

            # Check if lines have a red pixel
            # If pixel has a red color value, 
            # stop count and send to comparison statement
            if (b1, g1, r1) == (0,0,255):
                # print(count1)
                redpos1 = count1

            # if pixel is not red, go to the next one
            else:
                count1 = count1 + 1
            if (b2, g2, r2) == (0,0,255):

                # print(count2)
                redpos2 = count2
            else:
                count2 = count2 + 1
        
        # count1 is the right line and count2 is the left line
        print("2nd Count1", redpos1, "2nd Count2:", redpos2)
        if redpos1 > redpos2:
            # Robot turns left
            print("Turn Left")
        else:
            pass
        if redpos1 < redpos2:
            # Robot turns right
            print("Turn Right")
        else:
            pass
        if redpos1 == redpos2:
            # Robot goes straight
            print("Go straight")
        else:
            pass

        # Draw probe lines over probabalistic hough line mask.
        probes = np.copy(compvis)
        probes = cv2.line(probes, pt1 = (100,300), pt2 = (100, 230), color=(0,255,0), thickness= 1)
        probes = cv2.line(probes, pt1 = (200,300), pt2 = (200, 230), color=(0,255,0), thickness= 1)

        # stop time for filtering
        endFiltTime = time.time()
        print(f"Runtime for Filtering is:{endFiltTime - startFiltTime}")

        # Show frames for testing. Frames are shown in order of masking.
        cv2.imshow("Image",imgOut)
        cv2.imshow("Segmentation Capture", segImg)
        # cv2.imshow("Blue Mask", blueMask)
        # cv2.imshow("Resulting mask", result)
        cv2.imshow('Edges', edges)
        cv2.imshow('Hough Lines',copEdges)
        cv2.imshow('Fullscale',probes)
        
        # Delay Frame Input Rate based on testing
        time.sleep(0.2)

        # break program when ready
        if cv2.waitKey(1) == ord('q'):
            break
            

