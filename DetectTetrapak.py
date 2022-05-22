import cv2
import numpy as np
from FrameExtractor import *

def DetectTetrapak(path):
    # y1=500
    # y2=860
    # x1=1500
    # x2=1920

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    # roi = img[y1:y2, x1:x2]        #region of interest 

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),1)
    threshold = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)[1] #apply global thresholding
    canny=cv2.Canny(threshold,10,50)
    contours =cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through contours to find rectangles with area range of tetrapak
    cntrRect = []
    TetrapakCOM = []
    for i in contours:
            area = cv2.contourArea(i)
            # print(area) #debug
            if ((area > 20000)):
                epsilon = 0.05*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                if len(approx) > 4:
                    # print(area) #debug
                    cntrRect.append(approx)
                    # cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
    
    # print("Number of rec found = " + str(len(cntrRect)))    #debug
    for i in cntrRect:
        area = cv2.contourArea(i)   #debug
        # print(area)                 #debug
        M = cv2.moments(i)
        cX = int(M["m10"] / M["m00"]) #+ x1 #trimmed comment out
        cY = int(M["m01"] / M["m00"]) #+ y1 #trimmed comment out
        # draw the contour and center of the shape on the image
        cv2.drawContours(img,cntrRect,-1,(0,255,0),2)
        # cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
        # cv2.putText(img, "Tetrapak", (cX - 90 , cY - 65),
        #     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # img = DrawLanes(img, cY)
        TetrapakCOM.append([cX, cY])
    return img, TetrapakCOM

if __name__ == '__main__':
    try:    # delete later :)
        img, tetrapakstore = DetectTetrapak("framesTrimmed/frames290.jpg")
        print(tetrapakstore)
        for i in tetrapakstore:
            xcom, ycom = i
            print("Tetrapak centered at " + str(tetrapakstore[0][0]) + "," + str(tetrapakstore[0][1]))
        cv2.imshow('Detected tetrapak',img)
        cv2.waitKey(0)
    except:
        print("no tetrapak at this frame")