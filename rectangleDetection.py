import numpy as np
import cv2
import sys

def detectShape(c, fault_tolerance_in_px):

	# initialize the shape name and approximate the contour

	shape = "unidentified"
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

	tmpApprox = np.array([approx]).flatten()
	tmpApprox = np.sort(tmpApprox)

	rect = cv2.minAreaRect(c)
	box = cv2.boxPoints(rect)
	box = np.int0(box)

	tmpBox = np.array([box]).flatten()
	tmpBox = np.sort(tmpBox)

	if (cv2.contourArea(c) < 10):
		return ""


	# if the shape is a triangle, it will have 3 vertices
	if len(approx) == 3:
		shape = "triangle"

	# if the shape has 4 vertices, it is a rectangle
	elif len(approx) == 4:
		tmpDiff = abs(tmpApprox - tmpBox)
		if (all(tmpDiff <= fault_tolerance_in_px)):
			shape = "rectangle"
		else:
			shape = "quadrangle"

	# if the shape is a pentagon, it will have 5 vertices
	elif len(approx) == 5:
		shape = "pentagon"

	# otherwise, we assume the shape is a circle
	else:
		shape = "circle"

	return shape

def createColorMask(image, red, green, blue, percentage):
	
	upperRed = red + 255 * percentage
	upperBlue = blue + 255 * percentage
	upperGreen = green + 255 * percentage

	upper = np.array([upperBlue, upperGreen, upperRed])
	upper[upper > 255] = 255
	upper[upper < 0] = 0
	upper = np.int0(upper)

	lowerRed = red - 255 * percentage
	lowerBlue = blue - 255 * percentage
	lowerGreen = green - 255 * percentage

	lower = np.array([lowerBlue, lowerGreen, lowerRed])
	lower[lower < 0] = 0
	lower[lower > 255] = 255
	lower = np.int0(lower)

	colorMask = cv2.inRange(image, lower, upper)

	return colorMask

# parameters as read from the command line:
# path to image, red, green, blue, percentage, fault_tolerance_in_px, resulting_image_path
# red, green, blue -> color of the rectangle we're looking for
# percentage -> acceptable deviation from the rectangle's color, values between 0 and 1, typically 0.1
# fault_tolerance_in_px -> when determining if the shape is rectangluar and not quadrangle what is the allowed deviation in pixels from the bounding rectangle, typically 10
# resulting_image_path -> where to store the image with contours

def main():

	# load parameters

	image_path = sys.argv[1]
	red = np.int0(sys.argv[2])
	green = np.int0(sys.argv[3])
	blue = np.int0(sys.argv[4])
	percentage = np.float(sys.argv[5])
	fault_tolerance_in_px = np.int0(sys.argv[6])
	resulting_image_path = sys.argv[7]
	
	# load image	

	image = cv2.imread(image_path)

	# create color mask

	color_mask = createColorMask(image, red, green, blue, percentage)

	# leave only image areas that are of predefined color

	output = cv2.bitwise_and(image, image, mask = color_mask)

	# convert resulting image to grayscale to be able to apply findContours function

	output = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
	img, contours, hierarchy = cv2.findContours(output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	count = 0

	# for each contour detect shape and draw border around it if rectangle

	for c in contours:
		# draw the contour and show it
		contour_type = detectShape(c, fault_tolerance_in_px)
		if contour_type == "rectangle":
			cv2.drawContours(image, [c], -1, (255, 150, 255), 4)
			count += 1

	# write image to file

	cv2.imwrite(resulting_image_path, image)

	# print total number of rectangles of given color

	print("Total number of found rectangles: ")
	print(count)
	
if __name__ == "__main__":
	main()