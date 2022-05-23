import cv2
import os

#global variables
xPickup = 233 + 780       #pickup point will be at x = 233 from ROI

#60 to 400 = 340, thf. 340/4 = 85 (splitting conveyor into 4 equal vertical sections)
laneTop = 60 + 450
laneLower1 = laneTop + 85
laneLower2 = laneLower1 + 85
laneLower3 = laneLower2 + 85
laneBottom = 400 + 450

# Converts the conveyor feed video into a series of frames and saves them to ~/frames
def FrameExtractor(path):
    # os.makedirs("framesTrimmed", exist_ok=True)    # Creates folder ~/framesTrimmed if not preexisting
    os.makedirs("frames", exist_ok=True)    # Creates folder ~/frames if not preexisting
    os.makedirs("output", exist_ok=True)    # Creates folder ~/output if not preexisting
    
    video = cv2.VideoCapture(path)
    frameNum = 0
    success = 1

    while success:
        success, image = video.read()
        try:
            # y1=450
            # y2=880
            # x1=780
            # x2=1780
            # roi = image[y1:y2, x1:x2]   #trim video to save computing power
            
            # cv2.imwrite("framesTrimmed/frames%d.jpg" % frameNum, roi)
            cv2.imwrite("frames/frames%d.jpg" % frameNum, image)
            frameNum += 1
            print("Processing frame ", frameNum)
        except:
            print("Frame " + str(frameNum) + " empty or nonexistant.")

def DrawLanes(img):
    yBeltLower = 410 + 450
    yBeltUpper = 40 + 450
    image = cv2.line(img, (xPickup, yBeltUpper), (xPickup, yBeltLower), (0, 128, 265), 3)

    image = cv2.line(image, (xPickup-20, laneTop), (xPickup+20, laneTop), (265, 128, 0), 3)
    image = cv2.line(image, (xPickup-20, laneLower1), (xPickup+20, laneLower1), (265, 128, 0), 3)
    image = cv2.line(image, (xPickup-20, laneLower2), (xPickup+20, laneLower2), (265, 128, 0), 3)
    image = cv2.line(image, (xPickup-20, laneLower3), (xPickup+20, laneLower3), (265, 128, 0), 3)
    image = cv2.line(image, (xPickup-20, laneBottom), (xPickup+20, laneBottom), (265, 128, 0), 3)
    return image

def DetectLanes(yCOM):

    lane = 1
    if ((yCOM < laneLower1) and (yCOM >= laneTop)):
        lane = 1
    if ((yCOM < laneLower2) and (yCOM >= laneLower1)):
        lane = 2
    if ((yCOM < laneLower3) and (yCOM >= laneLower2)):
        lane = 3
    if ((yCOM <= laneBottom) and (yCOM >= laneLower3)):
        lane = 4
    return lane

def checkFor2Seconds(speed, xPos, yPos, objType, frameNum):
    xPickup = 233 + 780
    if speed > 0:
        timeToPickup = (xPos - xPickup)/speed
        if (timeToPickup <= 2):
            time = frameNum/30.0
            print(f'It is now { time:.2f}' + " seconds:")
            lane = DetectLanes(yPos)
            print(objType + " centered at " + str(xPos) + "," + str(yPos) + " will be arriving at pickup point at lane " + str(lane) +  f'in 2 seconds with speed of {speed:.2f}' + " pixels/second.")
            return True

if __name__ == '__main__':
    FrameExtractor("conveyor_feed.mp4")
    print("Frame processing complete.")
