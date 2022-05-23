import cv2
import numpy as np
from FrameExtractor import *

def DetectTetrapak(img):
    y1=450
    y2=880
    x1=780
    x2=1780

    roi = img[y1:y2, x1:x2]        #region of interest 

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),1)
    threshold = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)[1] #apply global thresholding
    canny=cv2.Canny(threshold,10,50)
    contours =cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through contours to find rectangles with area range of tetrapak
    cntrRect = []
    tetrapakCOM = []
    tetrapakAngle = []
    for i in contours:
            area = cv2.contourArea(i)
            # print(area) #debug
            if ((area > 20000)):
                epsilon = 0.05*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                if len(approx) > 4:
                    cntrRect.append(approx)

    for i in cntrRect:
        area = cv2.contourArea(i)   #debug
        # print(area)                 #debug
        M = cv2.moments(i)
        cX = int(M["m10"] / M["m00"]) + x1 #trimmed comment out
        cY = int(M["m01"] / M["m00"]) + y1 #trimmed comment out
        # draw the contour and center of the shape on the image
        cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
        tetrapakCOM.append([cX, cY])

        #get rotated rectangle
        rotrect = cv2.minAreaRect(cntrRect[0])
        box = cv2.boxPoints(rotrect)
        box = np.int0(box)

        # draw rotated rectangle on copy of img as result
        result = img.copy()
        cv2.drawContours(result,[box],0,(0,0,255),2)

        # get angle from rotated rectangle
        angle = rotrect[-1]

        # `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)
        
        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle
        tetrapakAngle.append(angle)

    return img, tetrapakCOM, tetrapakAngle

if __name__ == '__main__':
    img = cv2.imread("frames/frames290.jpg", cv2.IMREAD_COLOR)
    img, tetrapakstore, tetraAngle = DetectTetrapak(img)
    print(tetraAngle)
    for i in tetrapakstore:
        xcom, ycom = i
        print("Tetrapak centered at " + str(tetrapakstore[0][0]) + "," + str(tetrapakstore[0][1]))
    cv2.imshow('Detected tetrapak',img)
    cv2.waitKey(0)