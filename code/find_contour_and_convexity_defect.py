import cv2
import numpy as np
import math as m

def mod(a) :
	'''
		this method is used to find the square root of norm2 of a vector
	'''
	return m.sqrt(a[0]**2 + a[1]**2)

def find_angle(s,f,e) :
	'''
		this method is used to find the angle between two vectors
	'''
	s = np.array(np.float32(s))
	e = np.array(np.float32(e))
	f = np.array(np.float32(f))
	a = s-f
	b = e-f
	a = a/mod(a)
	b = b/mod(b)
	dot = np.dot(a, b)
	return m.acos(dot)*180/m.pi


def find_contour_and_convexity_defect(im,imgray):
	'''
		binarise the image on the basis of the threshold 127
	'''
	ret,thresh = cv2.threshold(imgray,127,255,0)
	
	#find countours on the binary image using the opencv draw_countours method
	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	#an array storing the length of countours found using findContours
	c = [len(c) for c in contours]

	#draw the contours on the image
	cv2.drawContours(im, [contours[c.index(max(c))]], 0, (0,255,0), 1)

	#only consider the contour having the largest number of points
	cnt = [contours[c.index(max(c))]][0]

	#draw convexhull on the contours enclosing the hand
	hull = cv2.convexHull(cnt,returnPoints = False)

	#find the convexity defectsin the convex hull
	defects = cv2.convexityDefects(cnt,hull)

	#count of the number of the filtered defects
	c = 0
	
	if(defects == None) :
		'''
			return a tupple using the image and the count if there are no defects
		'''
		return (im, c)

	for i in range(defects.shape[0]):
		'''
			for each convexity defects we have the start point the farthest point and
			the end point
		'''
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])

		#draw the convex hull edge corresponding to the convex defects
		cv2.line(im,start,end,[0,255,0],2)
		#find the angle of the convex hull defect
		angle = (find_angle(list(cnt[s][0]), list(cnt[f][0]), (cnt[e][0])))		
		if(angle < 90) :
			'''
				only consider a defect if the angle corresponding to it is less
				than 90 degree
			'''
			c += 1
			#mark the points on the convex hull and the convex defects
			cv2.circle(im,start,5,[0,255,255],-1)
			cv2.circle(im,end,5,[0,255,255],-1)
			cv2.circle(im,far,5,[0,0,255],-1)
	return (im, c)
