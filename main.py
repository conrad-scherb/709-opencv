from DetectLid import *
from DetectTetrapak import *
from DetectRoll import *
from ObjectTracker import *
from FrameExtractor import *
import cv2

frameNum = 0 #3170 #2300 #6000 # 0

trackerTetrapak = ObjectTracker()
trackerRoll = ObjectTracker()
trackerLid = ObjectTracker()
# obj_ids_tetrapak = trackerTetrapak.update([], frameNum)

while True:
    print("current frame: frames%d.jpg" % frameNum)
    img = cv2.imread("framesTrimmed/frames%d.jpg" % frameNum, cv2.IMREAD_COLOR)

    img, StoreLid = DetectLid(img)
    # print(StoreLid)
    obj_ids_lid = trackerLid.update(StoreLid, frameNum)
    if (len(obj_ids_lid) != 0):
        for obj_id in obj_ids_lid:  #obj_id = [x,y, id]a
            cX, cY, id, speed = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Lid", (cX - 10 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 10 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            print("Lid centered at " + str(cX) + "," + str(cY))
            checkFor2Seconds(speed, cX, cY, "Roll", frameNum)

    img, StoreTetrapak = DetectTetrapak(img)
    obj_ids_tetrapak = trackerTetrapak.update(StoreTetrapak, frameNum)
    if (len(obj_ids_tetrapak) != 0):
        for obj_id in obj_ids_tetrapak:  #obj_id = [x,y, id]
            cX, cY, id, speed = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Tetrapak", (cX - 90 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 90 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            # xPickup = 233
            checkFor2Seconds(speed, cX, cY, "Tetrapak", frameNum)
            # if speed > 0:
            #     timeToPickup = (cX - xPickup)/speed
            #     if (timeToPickup <= 2):
            #         time = frameNum/30.0
            #         print("it is now " + str(time) + " seconds:")
            #         print("Tetrapak centered at " + str(cX) + "," + str(cY) + " will be")
            #         DetectLanes(cY)
    
    img, StoreRoll = DetectRoll(img)
    # print(StoreRoll)
    obj_ids_roll = trackerRoll.update(StoreRoll, frameNum)
    if (len(obj_ids_roll) != 0):
        for obj_id in obj_ids_roll:  #obj_id = [x,y, id]
            cX, cY, id, speed  = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Paper roll", (cX - 60 , cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 60 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            checkFor2Seconds(speed, cX, cY, "Roll", frameNum)
            # xPickup = 233
            # if speed > 0:
            #     timeToPickup = (cX - xPickup)/speed
            #     if (timeToPickup <= 2):
            #         time = frameNum/30.0
            #         print("it is now " + str(time) + " seconds:")
            #         print("Roll centered at " + str(cX) + "," + str(cY) + " will be")
            #         DetectLanes(cY)

    # img2, StoreRolls = DetectRoll("framesTrimmed/frames%d.jpg" % frameNum)
    # obj_idsRoll = trackerRoll.update(StoreRolls)
    # for obj_idRoll in obj_idsRoll:
    #     cX, cY, id = obj_idRoll
    #     cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
    #     cv2.putText(img, "roll", (cX - 90 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    #     cv2.putText(img, ("[%d]" %id), (cX - 90 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    img = DrawLanes(img)
    cv2.imshow("no Lid", img)
    cv2.waitKey(0)
    # if frameNum < 2301:
    frameNum += 3

    key = cv2.waitKey(3)
    if key == 27:
        break

cv2.destroyAllWindows
