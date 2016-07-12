import cv2
import numpy as np

def creatDict(x, y) :
	'''
		create a dict containing the top two coordinates of the sqaure
	'''
	box = {}
	box['topx'] = x
	box['topy'] = y
	return box

def generateCenterBox(img, factor, sz) :
    '''
        this method returns 9 rectangles at the center of the bounding box
        from which we sample colours and return this sqaures as
        (leftx, lefty) each has a witdth sz and return as dict 
    '''
    w, h, channels = img.shape
    sw = w/factor
    sh = h/factor
    mtopx = w/2-sw/2
    mtopy = h/2-sh/2
    listOfBoxes = []
    listOfBoxes.append(creatDict(mtopx, mtopy))
    listOfBoxes.append(creatDict(w/2-sz/2, mtopy))
    listOfBoxes.append(creatDict(w/2+sw/2-sz, mtopy))
    listOfBoxes.append(creatDict(mtopx, h/2-sz/2))
    listOfBoxes.append(creatDict(w/2-sz/2, h/2-sz/2))
    listOfBoxes.append(creatDict(w/2+sw/2-sz, h/2-sz/2))
    listOfBoxes.append(creatDict(mtopx, h/2+sh/2-sz/2))
    listOfBoxes.append(creatDict(w/2-sz/2, h/2+sh/2-sz))
    listOfBoxes.append(creatDict(w/2+sw/2-sz, h/2+sh/2-sz))
    return listOfBoxes
