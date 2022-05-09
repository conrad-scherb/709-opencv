import cv2
import numpy as np

def DetectLid(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    dark_orange = np.array([0, 80, 80])
    light_orange = np.array([25, 255, 255])

    mask = cv2.inRange(hsv, dark_orange, light_orange)
    masked = cv2.bitwise_and(img, img, mask = mask)

    h, s, v = cv2.split(masked)

    detected_circles = cv2.HoughCircles(v, 
        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
        param2 = 30, minRadius = 1, maxRadius = 40)
    
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
    
            cv2.rectangle(img, (a-r-5, b-r-5), (a+r+5, b+r+5), (0, 255, 0), 2)
            cv2.putText(img, 'Lid', (a-r-5, b-r-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Detected Lid", img)
            cv2.waitKey(0)

if __name__ == '__main__':
    DetectLid("frames/frames134.jpg")