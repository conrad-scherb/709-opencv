from DetectRoll import *

def CalculateRollSpeed(startingFrame, span):
    fps = 30

    path1 = "framesTrimmed/frames" + str(startingFrame) + ".jpg"
    img1 = cv2.imread(path1, cv2.IMREAD_COLOR)
    path2 = "framesTrimmed/frames" + str(startingFrame+span) + ".jpg"
    img2 = cv2.imread(path2, cv2.IMREAD_COLOR)

    img1, com1 = DetectRoll(img1)
    img2, com2 = DetectRoll(img2)

    time = span/fps
    x1 = com1[0][0]
    x2 = com2[0][0]

    return abs(x1-x2)/time, x1

def CalculateTimePickupRoll(startingFrame, span):
    speed, xObj = CalculateRollSpeed(startingFrame,span)
    print(str(speed) + " pixels per second")
    # t = d/v
    xPickup = 233
    # print(str(xObj-xPickup))
    timePickup = (xObj-xPickup)/speed
    return timePickup

if __name__ == '__main__':
    test = 0
    startFrame = 100
    while test == 0:
        try:
            
            time = CalculateTimePickupRoll(startFrame, 30)      #this is the time from the start frame i think
            print("roll will reach pickup point in " + str(time) + " seconds.")
            
            #TODO: change speed to an average function maybe since sometimes the conveyor slows down
            #TODO: the specific frame that the timing actually starts from isnt saved if input too early frame (no object)
            #TODO: the 2 second befor pickup thing

            test = 1
        except:
            print("there is no roll at frame " , startFrame)
            startFrame += 1