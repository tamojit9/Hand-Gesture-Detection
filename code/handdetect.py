#!/usr/bin/env python

'''
face detection using haar cascades

USAGE:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import math as m
import findmediannew as f
from subprocess import call

# local modules
from video import create_capture
from common import clock, draw_str

def detect(img, cascade):
    '''
        this method is used to find the objects embedded in the image
        using the haar classifier we have trained 
    '''
    rects = cascade.detectMultiScale(img, scaleFactor=3, minNeighbors=10, minSize=(50, 50),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


def draw_rects(img, rects, color):
    '''
        tihs method draws the rectangle on the detected hand and also marks the hand 
        with all the convex hull points, convexity defects 
    '''
    if(len(rects) > 1) :
        return (img,0)
    for x1, y1, x2, y2 in rects:
        h = abs(y2-y1)
        w = abs(x2-x1)
        if(h < 50 or h > 150 or w < 50 or w > 150) :
            continue
        crop_img = img[y1:(y1+h), x1:(x1+w)]
        img[y1+3:(y1+h-h/5), x1+3:(x1+w-6)],c = f.preprocessImage(crop_img)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        return (img,c)

def checkstability(a) :
    '''
        find which finger-count has the maximum occurence in the last
        few frames and return that.
        This is used to stop the software from random changes in the
        the finger-count
    '''
    cnt = [0,0,0,0,0,0]
    for i in range(len(a)-1, 0, -1) :
        cnt[a[i]] += 1
    return cnt.index(max(cnt))


#main logic block

if __name__ == '__main__':
    import sys, getopt
    print(__doc__)

    '''
        takes command line arguments for the source of the video capture
        (by default laptop video camera) and the cascade file which is used to detect objects.
    '''
    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    

    try:
        '''
            checks to see if a source for video capture is provided as argument
            or 
            than tries the webcam of the laptop
        '''
        video_src = video_src[0]
    except:
        video_src = 0
    args = dict(args)

    '''
        gets the cascade file from either command line argument or the default location
    '''
    cascade_fn = args.get('--cascade', "../../data/haarcascades/cascade.xml")
    

    cascade = cv2.CascadeClassifier(cascade_fn)
    
    '''
        if the video source is not found than the video capture source falls back to
        the image file of lena.jpg and runs image detection on this image
    '''
    cam = create_capture(video_src, fallback='synth:bg=../data/lena.jpg:noise=0.05')
    
    #array of count of fingers found in the last few frames
    cs = []
    
    #count of fingers found in the current frame
    c = 0

    '''
        this variable is used to stop the same action from happening again and again
        like keep on opening new tabs if the finger count remains the same
    '''
    done = -1


    while True:
        #the main video capture loop

        #reseting the finger count variable every time
        c = 0

        #read the image from camera 
        ret, img = cam.read()

        #read convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        '''
            histogram equalisation to normalise the contrast and make detection robust to
            high or low contrasted images
        '''
        gray = cv2.equalizeHist(gray)
        
        '''
            use the HAAR classifier to detect the objects and return the bounding rectangles
            of the objects detected in the image
        '''
        rects = detect(gray, cascade)

        vis = img

        '''
            draw_rects method darws the rectangles in the image and processes the image
            to find the fingures in the hand and marks them
        '''
        stuff = draw_rects(vis, rects, (0, 255, 0))


        if(stuff != None) :
            '''
                get the count of the fingure returned by the draw_rects method
            '''
            c = stuff[1]
            #append the count to the array of fingure counts
            cs.append(c)

        #draw the number of fingers on the screen
        draw_str(vis, (20, 20), 'number of fingers =: %d' % (c+1))

        #draw the final image on the screen
        cv2.imshow('fingers', vis)

        #detect if escape is pressed and exist from the image
        if 0xFF & cv2.waitKey(5) == 27:
            break

        #find out if there are enough fingure counts in the array
        if(len(cs) > 2) :
            '''
                check which fingure count is the most and execute the action corresponding
                to that
            '''
            c = checkstability(cs)
            cs = []
        else :
            continue

        '''
            map fingure count to corresponding actions in the software
        '''    
        if(c == 2) :
            vis = cv2.cvtColor(vis, cv2.COLOR_BGR2GRAY)
            if(done != c) :
                call(["google-chrome", "cse.iitb.ac.in"])
            done = c
        elif(c == 4) :
            vis = cv2.blur(vis, (5,5))
            if(done != c) :
                call(["google-chrome", "www.facebook.com"])
                done = False
            done = c
        elif(c == 3) :
            vis = cv2.cvtColor(vis,cv2.COLOR_BGR2HSV)
            if(done != c) :
                call(["google-chrome", "www.youtube.com"])
            done = c
    cv2.destroyAllWindows()
