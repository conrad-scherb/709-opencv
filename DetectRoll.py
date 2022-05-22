import cv2
import numpy as np
from FrameExtractor import *

def adjust_gamma(image, gamma=1.0): #gamma function

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

def DetectRoll(img):
    # y1=500
    # y2=860
    # x1=1500
    # x2=1920

    # img = cv2.imread(path, cv2.IMREAD_COLOR)
    # roi = img[y1:y2, x1:x2]     #region of interest 

    gamma = 0.85                # darken image to exclude roll shadow
    adjusted = adjust_gamma(img, gamma=gamma)

    dark_brown = np.array([0, 0, 150])
    light_brown = np.array([100, 200, 255])
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, dark_brown, light_brown)
    masked = cv2.bitwise_and(img, img, mask = mask)

    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    threshold = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)[1] #apply global thresholding
    canny=cv2.Canny(threshold,10,50)
    contours =cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through contours to find rectangles with area range of roll
    cntrRect = []
    rollCOM = []
    for i in contours:
            area = cv2.contourArea(i)
            # print(area) #debug
            if ((area > 3500) and (area <4300)):
                epsilon = 0.05*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                if len(approx) == 4:
                    # print(area) #debug
                    cntrRect.append(approx)
                    # print(approx)
                    # cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
    
    # print("Number of rec found = " + str(len(cntrRect)))    #debug
    for i in cntrRect:
        area = cv2.contourArea(i)   #debug
        # print(area)                 #debug
        M = cv2.moments(i)
        cX = int(M["m10"] / M["m00"]) #+ x1     #comment out +x1 if trimmed frame
        cY = int(M["m01"] / M["m00"]) #+ y1     #comment out +y1 if trimmed frame
        # draw the contour and center of the shape on the image
        cv2.drawContours(img,cntrRect,-1,(0,255,0),2)
        # cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
        # cv2.putText(img, "Paper roll", (cX - 60 , cY - 40),
        #     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # img = DrawLanes(img, cY)
        rollCOM.append([cX, cY])
    return img, rollCOM

if __name__ == '__main__':
    img = cv2.imread("framesTrimmed/frames1700.jpg", cv2.IMREAD_COLOR)
    # img, cX, cY = DetectRoll("framesTrimmed/frames5000.jpg")
    # print("Paper roll centered at " + str(cX) + "," + str(cY))
    img, rollstorage = DetectRoll(img)
    print(rollstorage)
    for i in rollstorage:
        xcom, ycom = i
        print("Paper roll centered at " + str(xcom) + "," + str(ycom))

    cv2.imshow('Detected Paper Roll',img)
    cv2.waitKey(0)

# try:    # delete later :)
#     if __name__ == '__main__':
#         # img, cX, cY = DetectRoll("framesTrimmed/frames5000.jpg")
#         # print("Paper roll centered at " + str(cX) + "," + str(cY))
#         img, rollstorage = DetectRoll("framesTrimmed/frames5000.jpg")
#         print(rollstorage)
#         for i in rollstorage:
#             xcom, ycom = rollstorage[i]
#             print(xcom)
#             print(ycom)


#         cv2.imshow('Detected Paper Roll',img)
#         cv2.waitKey(0)
# except:
#     print("no roll at this frame")
