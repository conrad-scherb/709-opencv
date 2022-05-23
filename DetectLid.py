import cv2
import numpy as np
from FrameExtractor import *

def DetectLid(img):
    # img = cv2.imread(path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    dark_blue = np.array([50, 150, 0])
    light_blue = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, dark_blue, light_blue)
    masked = cv2.bitwise_and(img, img, mask = mask)

    h, s, v = cv2.split(masked)

    cv2.imshow("lid", masked)
    cv2.waitKey(0)

    detected_circles = cv2.HoughCircles(v, 
        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
        param2 = 30, minRadius = 10, maxRadius = 18)
    
    LidCOM = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
    
            cv2.circle(img, (a, b), 15, (0, 255, 0), 2)
            # cv2.putText(img, 'Lid', (a-r-5, b-r-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # cv2.circle(img, (a, b), 7, (0, 255, 0), -1)
            # img = DrawLanes(img, b)
            LidCOM.append([a, b])
    return img, LidCOM

if __name__ == '__main__':
    img = cv2.imread("framesTrimmed/frames1700.jpg", cv2.IMREAD_COLOR)
    img, LidStorage = DetectLid(img)
    print(LidStorage)
    for i in LidStorage:
        xcom, ycom = i
        print("Lid centered at " + str(xcom) + "," + str(ycom))
    cv2.imshow("Detected Lid", img)
    cv2.waitKey(0)
