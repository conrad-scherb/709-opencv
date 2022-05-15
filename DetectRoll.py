import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0): #gamma function

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

def DetectRoll(path):
    y1=500
    y2=860
    x1=1500
    x2=1920

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    roi = img[y1:y2, x1:x2] #region of interest 

    gamma = 0.85                                   # darken image to exclude roll shadow
    adjusted = adjust_gamma(roi, gamma=gamma)
    cv2.imshow("gamma image", adjusted)
    cv2.waitKey(0)

    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY) #convert roi into gray

    cv2.imshow("gray image", gray)
    cv2.waitKey(0)

 
    Blur=cv2.GaussianBlur(gray,(5,5),1) #apply blur to gray roi
    cv2.imshow("blur", Blur)
    cv2.waitKey(0)

    ret,th1 = cv2.threshold(Blur,127,255,cv2.THRESH_BINARY) #apply global thresholding

    cv2.imshow("global thresholding gaussian smoothing", th1)
    cv2.waitKey(0)

    Canny=cv2.Canny(th1,10,50) #apply canny to roi

    cv2.imshow("canny image", Canny)
    cv2.waitKey(0)

    #Find my contours
    contours =cv2.findContours(Canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

    #Loop through contours to find rectangles with area range of roll
    cntrRect = []
    for i in contours:
            area = cv2.contourArea(i)
            # print(area) #debug
            if ((area > 3500) and (area <4300)):
                epsilon = 0.05*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                if len(approx) == 4:
                    print(area)
                    cntrRect.append(approx)
                    # cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
    
    print("Number of rec found = " + str(len(cntrRect)))    #debug
    for i in cntrRect:
            area = cv2.contourArea(i)   #debug
            print(area)                 #debug
            M = cv2.moments(i)
            cX = int(M["m10"] / M["m00"]) + x1
            cY = int(M["m01"] / M["m00"]) + y1
            # draw the contour and center of the shape on the image
            cv2.drawContours(roi,cntrRect,-1,(0,255,0),2)
            cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(img, "Roll center", (cX - 60 , cY - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            return img, cX, cY

try:    # delete later :)
    if __name__ == '__main__':
        img, cX, cY = DetectRoll("frames/frames3670.jpg")
        print("Paper roll centered at " + str(cX) + "," + str(cY))
        cv2.imshow('Detected Paper Roll',img)
        cv2.waitKey(0)
except:
    print("no roll at this frame")
