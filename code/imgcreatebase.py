import Image
import cv2
import numpy as np
def sumAndBlurImg(img):
	'''
		from the nine different binary images create one image using
		majority voting algorithm(a pixel becomes white if majority say so)
		finally blur the image to remove the extra noises and smoothen it
	'''
	a, b = img[0].shape
	pixels = np.zeros((a, b))
	for i in range(0, a):
		for j in range(0, b):
			c = 0
			for k in range(0, len(img)):
				if(img[k][i,j] == 255 ):
					c += 1
			if(c > len(img)/2) :
				pixels[i, j] = 255
	
	pixels = cv2.blur(pixels,(5,5))
	return pixels

	




