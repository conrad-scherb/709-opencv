from DetectBox import *

def CalculateBoxSpeed(startingFrame, span):
    fps = 30

    path1 = "frames/frames" + str(startingFrame) + ".jpg"
    path2 = "frames/frames" + str(startingFrame+span) + ".jpg"

    img1, x1, y1 = DetectBox(path1)
    img2, x2, y2 = DetectBox(path2)

    time = span/fps

    return abs(x1-x2)/time

if __name__ == '__main__':
    speed = CalculateBoxSpeed(134, 30)
    print(str(speed) + " pixels per second")