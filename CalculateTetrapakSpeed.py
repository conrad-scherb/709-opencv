from DetectTetrapak import *

def CalculateTetrapakSpeed(startingFrame, span):
    fps = 30

    path1 = "frames/frames" + str(startingFrame) + ".jpg"
    path2 = "frames/frames" + str(startingFrame+span) + ".jpg"

    img1, x1, y1 = DetectTetrapak(path1)
    img2, x2, y2 = DetectTetrapak(path2)

    time = span/fps

    return abs(x1-x2)/time

test = 0
startFrame = 150
while test == 0:
    try:
        if __name__ == '__main__':
            speed = CalculateTetrapakSpeed(startFrame, 30)
            print(str(speed) + " pixels per second")
            test = 1
    except:
        print("there is no tetrapak at frame " , startFrame)
        startFrame += 1