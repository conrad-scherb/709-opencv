from DetectRoll import *

def CalculateRollSpeed(startingFrame, span):
    fps = 30

    path1 = "frames/frames" + str(startingFrame) + ".jpg"
    path2 = "frames/frames" + str(startingFrame+span) + ".jpg"

    img1, x1, y1 = DetectRoll(path1)
    img2, x2, y2 = DetectRoll(path2)

    time = span/fps

    return abs(x1-x2)/time

test = 0
startFrame = 100
while test == 0:
    try:
        if __name__ == '__main__':
            speed = CalculateRollSpeed(startFrame, 30)
            print(str(speed) + " pixels per second")
            test = 1
    except:
        print("there is no roll at frame " , startFrame)
        startFrame += 1