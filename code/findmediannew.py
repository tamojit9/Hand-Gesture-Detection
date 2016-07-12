# -*- coding: utf-8 -*-
import numpy as np
import generateBox as gb
import cv2
import binarize as b
import imgcreatebase as i
import find_contour_and_convexity_defect as dc

def findmedian(image,boxes,size) :
    '''
        find the median color of each of the nine rectangles and sample return
        them as a three lists for (R,G,B) each 
    '''
    lst=[]
    for corner in boxes:
        red=[]
        green=[]
        blue=[]
        l=[]
        '''
            iterate through each of the pixels of each box and find the median 
            of each of them
        '''
        for yval in range(corner['topy'],corner['topy']+size):
                for xval in range(corner['topx'],corner['topx']+size):
                    red.append(image[xval][yval][0])
                    green.append(image[xval][yval][1])
                    blue.append(image[xval][yval][2])
        '''
            sort each of the color pixels and find the median for each of them
        '''
        red.sort()
        green.sort()
        blue.sort()
        retind=(len(red)+1)/2
        l.append(red[retind])
        l.append(green[retind])
        l.append(blue[retind])
        lst.append(l)
    return lst


#--------------------------------------------testing-------------------------------------------------
def matToImg(im, img) :
    '''
        create a three channel image from a one channel image
    '''
    imc = np.zeros_like(img)
    imc[:,:,0] = im
    imc[:,:,1] = im
    imc[:,:,2] = im
    im = imc
    return im
def preprocessImage(img) :
    '''
        this is the main method the  integrates the whole alogithm and
        calls the various sub parts one by one to get the final result
    '''
    sz = 4
    h,w,_ = img.shape
    img = img[3:h-h/5,3:w-6]
    rects = gb.generateCenterBox(img, 3, sz)
    imgs = b.img_binarizer(img, findmedian(img, rects, sz))
    im = i.sumAndBlurImg(imgs)
    im = matToImg(im, img)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    modified_img = dc.find_contour_and_convexity_defect(im, imgray)
    return modified_img 
#---------------------------------------------testing------------------------------------------------
    



