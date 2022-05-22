from DetectTetrapak import *

def CalculateTetrapakSpeed(startingFrame, span):
    fps = 30

    path1 = "framesTrimmed/frames" + str(startingFrame) + ".jpg"
    path2 = "framesTrimmed/frames" + str(startingFrame+span) + ".jpg"

    img1, x1, y1 = DetectTetrapak(path1)
    img2, x2, y2 = DetectTetrapak(path2)

    time = span/fps

    return abs(x1-x2)/time, x1

def CalculateTimePickupTetrapak(startingFrame, span):
    speed, xObj = CalculateTetrapakSpeed(startingFrame,span)
    print(str(speed) + " pixels per second")
    # t = d/v
    xPickup = 233
    # print(str(xObj-xPickup))
    timePickup = (xObj-xPickup)/speed
    return timePickup

if __name__ == '__main__':
    test = 0
    startFrame = 848
    while test == 0:
        try:
            
            time = CalculateTimePickupTetrapak(startFrame, 30)      #this is the time from the start frame i think
            print("tetrapak will reach pickup point in " + str(time) + " seconds.")
            
            #TODO: change speed to an average function maybe since sometimes the conveyor slows down
            #TODO: the specific frame that the timing actually starts from isnt saved if input too early frame (no object)
            #TODO: the 2 second befor pickup thing

            test = 1
        except:
            print("there is no tetrapak at frame " , startFrame)
            startFrame += 1