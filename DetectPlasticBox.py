import cv2
import numpy as np
from FrameExtractor import *

def DetectPlasticBox(img):
    y1=450
    y2=880
    x1=780
    x2=1780
    # img = cv2.imread(path, cv2.IMREAD_COLOR)
    roi = img[y1:y2, x1:x2]     #region of interest 
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    dark_orange = np.array([0, 100, 100])
    light_orange = np.array([25, 255, 255])

    mask = cv2.inRange(hsv, dark_orange, light_orange)
    masked = cv2.bitwise_and(roi, roi, mask = mask)

    h, s, v = cv2.split(masked)

    detected_circles = cv2.HoughCircles(v, 
        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
        param2 = 30, minRadius = 35, maxRadius = 45)
    
    PlasticCOM = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = (pt[0]), (pt[1]), pt[2]
            cX = a + 780
            cY = b + 450
            cv2.rectangle(img, (cX-r-5, cY-r-5), (cX+r+5, cY+r+5), (0, 255, 0), 2)
            
            PlasticCOM.append([cX, cY])
    return img, PlasticCOM

if __name__ == '__main__':
    img = cv2.imread("frames/frames3140.jpg", cv2.IMREAD_COLOR)
    img, lidStorage = DetectPlasticBox(img)
    print(lidStorage)
    for i in lidStorage:
        xcom, ycom = i
        print("Plastic centered at " + str(xcom) + "," + str(ycom))
    cv2.imshow("Detected Plastic", img)
    cv2.waitKey(0)
