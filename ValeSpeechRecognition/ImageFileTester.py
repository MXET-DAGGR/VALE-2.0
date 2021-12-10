# Import necessary libraries below

import pixellib
from pixellib.semantic import semantic_segmentation
import cv2
import numpy as np

# Import sementation class
segment_frame = semantic_segmentation()

# Load segmentation model
segment_frame.load_ade20k_model("deeplabv3_xception65_ade20k.h5")

# Apply segmentation and save the image to a working directory
segment_frame.segmentAsAde20k("WorkingTest2.jpg", output_image_name = "NewWorking2.jpg", overlay = False, extract_segmented_objects=True)

# Read the saved image from the working directory
img = cv2.imread("NewWorking2.jpg")

# For testing
# print(img.shape)

# Resize the image
percent_scale = 15
width = int(img.shape[1] * percent_scale / 100)
height = int(img.shape[0] * percent_scale / 100)
dimensions = (width, height)
resized = cv2.resize(img,dsize = dimensions, interpolation=cv2.INTER_AREA)

# Make a copy of the image
imgcopy = np.copy(resized)

# Show the image for testing
cv2.imshow("resized",resized)

# apply color masks for segmenting out object within an image frame

# Gray and yellow masks from segmentation before manipulation of mask values within the pixellib library.
# lowerGray = np.array([139,139,139])
# upperGray = np.array([140,140,140])

# lowerYellow = np.array([7,254,235])
# upperYellow = np.array([8,255,236])

# Blue mask applied after manipulation of object mask values within pixellib library
lowerBlue = np.array([220,0,0])
upperBlue = np.array([255,1,1])

# Apply color masks to the resized image
# mask1 = cv2.inRange(resized,lowerGray,upperGray)
# mask2 = cv2.inRange(resized,lowerYellow,upperYellow)
blueMask = cv2.inRange(resized,lowerBlue, upperBlue)

# Apply filtering as needed
# result = cv2.bitwise_or(mask1,mask2,imgcopy)
# result2 = cv2.bitwise_and(resized,resized,mask3)
# kernel = np.ones((2,2), np.uint8)
# withDil = cv2.dilate(result,kernel,iterations = 5)
# edges = cv2.Canny(withDil,100,200)
# withDil[np.where((withDil==[255,255,255]).all(axis=2))]=[0,0,255]

# Apply masks and filtering to resized image to get final image results
# fullscale = cv2.bitwise_and(resized,resized,withDil,withDil)
fullscale2 = cv2.bitwise_and(resized,resized,blueMask,blueMask)

# Apply edge detector to fullscale results
edges2 = cv2.Canny(fullscale2,100,200)

# Show images for testing
# cv2.imshow("gray",mask1)
# cv2.imshow("yellow",mask2)
cv2.imshow("Blue", blueMask)
# cv2.imshow("result",result)
# cv2.imshow("blue result", result2)
# cv2.imshow("Fullscale",fullscale)
# cv2.imshow("Dialation",withDil)
# cv2.imshow("edges",edges)
cv2.imshow("edges2", edges2)
cv2.imshow("Fullscale2", fullscale2)

# Press any key to stop viewing testing images
cv2.waitKey(0)
cv2.destroyAllWindows()

