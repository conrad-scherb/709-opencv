import cv2
import numpy as np
from FrameExtractor import *

def DetectLid(img):
    y1=450
    y2=880
    x1=780
    x2=1780
    roi = img[y1:y2, x1:x2]     #region of interest 
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    dark_blue = np.array([50, 150, 0])
    light_blue = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, dark_blue, light_blue)
    masked = cv2.bitwise_and(roi, roi, mask = mask)

    h, s, v = cv2.split(masked)

    detected_circles = cv2.HoughCircles(v, 
        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
        param2 = 30, minRadius = 10, maxRadius = 18)
    
    LidCOM = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = (pt[0]), (pt[1]), pt[2]
            cX = a + 780
            cY = b + 450
            cv2.circle(img, (cX, cY), 15, (0, 255, 0), 2)
            LidCOM.append([cX, cY])
    return img, LidCOM

if __name__ == '__main__':
    img = cv2.imread("frames/frames1700.jpg", cv2.IMREAD_COLOR)
    img, LidStorage = DetectLid(img)
    print(LidStorage)
    for i in LidStorage:
        xcom, ycom = i
        print("Lid centered at " + str(xcom) + "," + str(ycom))
    cv2.imshow("Detected Lid", img)
    cv2.waitKey(0)
