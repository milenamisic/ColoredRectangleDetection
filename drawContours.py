import cv2
import numpy as np
import sys

imagePath = sys.argv[1]
result1Name = sys.argv[2]

# contour detection
img = cv2.imread(imagePath)

img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(img3, 127, 255, 0)
img4, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(img, contours, -1, (255,10,10), 2)

cv2.imwrite(result1Name, img)