import cv2
import numpy as np
from FrameExtractor import *

def adjust_gamma(image, gamma=1.0): #gamma function for shadows

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

def DetectRoll(img):
    y1=450
    y2=880
    x1=780
    x2=1780

    roi = img[y1:y2, x1:x2]     #region of interest 

    gamma = 0.85                # darken image to exclude roll shadow
    adjusted = adjust_gamma(roi, gamma=gamma)

    dark_brown = np.array([0, 0, 150])
    light_brown = np.array([100, 200, 255])
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, dark_brown, light_brown)
    masked = cv2.bitwise_and(roi, roi, mask = mask)

    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    threshold = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)[1] #apply global thresholding
    canny=cv2.Canny(threshold,10,50)
    contours =cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through contours to find rectangles with area range of roll
    cntrRect = []
    rollCOM = []
    rollAngle = []
    for i in contours:
            area = cv2.contourArea(i)
            if ((area > 3500) and (area <4300)):
                epsilon = 0.05*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                if len(approx) == 4:
                    cntrRect.append(approx)
    
    # print("Number of rec found = " + str(len(cntrRect)))    #debug
    for i in cntrRect:
        area = cv2.contourArea(i)   #debug
        # print(area)                 #debug
        M = cv2.moments(i)
        cX = int(M["m10"] / M["m00"]) + x1     #comment out +x1 if trimmed frame
        cY = int(M["m01"] / M["m00"]) + y1     #comment out +y1 if trimmed frame
        # draw the contour and center of the shape on the image
        cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
        rollCOM.append([cX, cY])

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

        # print(angle,"deg")
        rollAngle.append(angle)

    
    return img, rollCOM, rollAngle

if __name__ == '__main__':
    img = cv2.imread("frames/frames1700.jpg", cv2.IMREAD_COLOR)
    img, rollstorage, angle = DetectRoll(img)
    print(angle)
    for i in rollstorage:
        xcom, ycom = i
        print("Paper roll centered at " + str(xcom) + "," + str(ycom))

    cv2.imshow('Detected Paper Roll',img)
    cv2.waitKey(0)
