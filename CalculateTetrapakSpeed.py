from DetectTetrapak import *

def CalculateTetrapakSpeed(startingFrame, span):
    fps = 30

    path1 = "framesTrimmed/frames" + str(startingFrame) + ".jpg"
    path2 = "framesTrimmed/frames" + str(startingFrame+span) + ".jpg"

    img1, x1, y1 = DetectTetrapak(path1)
    img2, x2, y2 = DetectTetrapak(path2)

    time = span/fps

    return abs(x1-x2)/time, x2

def CalculateTimePickup(startingFrame, span):
    speed, xObj = CalculateTetrapakSpeed(startFrame,span)
    print(str(speed) + " pixels per second")
    # t = d/v
    xPickup = 233
    print(str(xObj-xPickup))
    timePickup = (xObj-xPickup)/speed
    return timePickup


test = 0
startFrame = 150
while test == 0:
    try:
        if __name__ == '__main__':
            time = CalculateTimePickup(startFrame, 30)
            print("tetrapak will reach pickup point in " + str(time) + " seconds.")
            #this is the time from the last frame i.e. startFrame+30 i think
            test = 1
    except:
        print("there is no tetrapak at frame " , startFrame)
        startFrame += 1