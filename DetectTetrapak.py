import cv2
import numpy as np

def DetectTetrapak(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0,0,245])
    upper_white = np.array([255,10,255])    

    mask = cv2.inRange(hsv, lower_white, upper_white)
    masked = cv2.bitwise_and(img, img, mask = mask)

    cv2.imshow("Detected Tetrapak", masked)
    cv2.waitKey(0)

if __name__ == '__main__':
    DetectTetrapak("frames/frames331.jpg")