import cv2
import numpy as np
import sys

imagePath = sys.argv[1]

# brightness & contrast

brightness = sys.argv[2]
contrast = sys.argv[3]

# result paths

result1Name = sys.argv[4]

img = cv2.imread(imagePath)
img1 = cv2.imread(imagePath)
img2 = img1

cv2.convertScaleAbs(img1, img2, float(contrast), int(brightness))

cv2.imwrite(result1Name, img2)