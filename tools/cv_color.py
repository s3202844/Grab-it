from scipy.spatial import distance as dist
from collections import OrderedDict
import imutils
import cv2
import numpy as np
import time

class ColorDetector:
	def __init__(self):
		colors = OrderedDict({
				"red": (255, 0, 0),
				"green": (0, 255, 0),
				"blue": (0, 0, 255),
				"yellow": (255, 255, 0)
			})

		self.lab = np.zeros((len(colors), 1, 3), dtype='uint8')
		self.colorNames = []

		for (i, (name, rgb)) in enumerate(colors.items()):
			self.lab[i] = rgb
			self.colorNames.append(name)
		
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_BGR2HSV)

	def shape(self, image):

		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# red, green, blue 
		boundaries = [
			# (np.array([21, 39, 64]), np.array([40, 255, 255])),
			(np.array([0, 43, 35]), np.array([10, 255, 255])),
			(np.array([41, 39, 64]), np.array([80, 255, 255])),
			(np.array([100, 43, 35]), np.array([124, 255, 255]) ),
		]

		for (i, color_range) in enumerate(boundaries):
			color_part = cv2.inRange(hsv, color_range[0], color_range[1])
			cv2.imwrite('./testimage.jpg', color_part)
			cnts = cv2.findContours(color_part, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)

			if len(cnts) > 0:
				print("color is:", i)
				break
	
	def detectColor(self):
		vid = cv2.VideoCapture(0)
		_, frame = vid.read()

		cv2.imwrite('./testimage.jpg', frame)
		
		height, width, _ = frame.shape
		
		center_x, center_y = int(width/2), int(height/2)
		
		start = (center_x - 100, center_y - 20 )
		end = (center_x, center_y + 20 )
		
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		total = 0
		true_r = 0
		true_y = 0
		true_g = 0
		true_b = 0
		for i in range(start[0], end[0], 5):
			for j in range(start[1], end[1], 5):
				total += 1
				hue_value = hsv[i,j,0]
				if 0 < hue_value < 9 or 159 < hue_value < 180:
					true_r += 1
					color = "RED"
				elif 21 < hue_value < 33:
					true_y += 1
					color = "YELLOW"
				elif 36 < hue_value < 89:
					true_g += 1
					color = "GREEN"
				elif 100 < hue_value < 128:
					true_b += 1
					color = "BLUE"
				else:
					color = "Nothing"
		
		# cv2.imshow("temp", frame)
		# cv2.waitKey(10)
		print(true_r, true_y, true_g, true_b, total)
		
		if true_r / total > 0.4:
			return 1
		
		if true_g / total > 0.4:
			return 2
		
		if true_b / total > 0.4:
			return 3
		
		if true_y / total > 0.4:
			return 4
		
###
# vid = cv2.VideoCapture(0)
# while True:
# 	_, frame = vid.read()

# 	height, width, _ = frame.shape

# 	center_x, center_y = int(width/2), int(height/2)

# 	start = (center_x - 100, center_y - 20 )
# 	end = (center_x, center_y + 20 )

# 	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 	total = 0
# 	true_r = 0
# 	true_g = 0
# 	true_b = 0
# 	for i in range(start[0], end[0], 5):
# 		for j in range(start[1], end[1], 5):
# 			total += 1
# 			hue_value = hsv[i,j,0]
# 			if 0 < hue_value < 9 or 159 < hue_value < 180:
# 				true_r += 1
# 				color = "RED"
# 			elif 21 < hue_value < 33:
# 				color = "YELLOW"
# 			elif 36 < hue_value < 89:
# 				true_g += 1
# 				color = "GREEN"
# 			elif 100 < hue_value < 128:
# 				true_b += 1
# 				color = "BLUE"
# 			else:
# 				color = "Nothing"
		
	
# 	if true_r / total > 0.6:
# 		print("it is red")
	
# 	if true_g / total > 0.6:
# 		print("it is green")
	
# 	if true_b / total > 0.6:
# 		print("it is blue")

# 			# print(cv2.inRange( [hsv[i, j]], np.array([41, 39, 64]), np.array([80, 255, 255])))


# 	# cv2.rectangle(frame, start, end, (25, 25, 25), 3)

#     # cube = CubeColor()

#     # cube.shape(frame)
# 	cv2.imshow("temp", frame)
# 	cv2.waitKey(10)
