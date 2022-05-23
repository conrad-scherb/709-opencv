from re import A
from DetectPlasticBox import *
from DetectLid import *
from DetectTetrapak import *
from DetectRoll import *
from ObjectTracker import *
from FrameExtractor import *

frameNum = 0 #3170 #2300 #6000 # 0

trackerTetrapak = ObjectTracker()
trackerRoll = ObjectTracker()
trackerPlastic = ObjectTracker()
trackerLid = ObjectTracker()

while True:
    img = cv2.imread("frames/frames%d.jpg" % frameNum, cv2.IMREAD_COLOR)

    img, StorePlastic = DetectPlasticBox(img)
    # print(StoreLid)
    obj_ids_plastic = trackerPlastic.update(StorePlastic, frameNum)
    if (len(obj_ids_plastic) != 0):
        for obj_id in obj_ids_plastic:  #obj_id = [x, y, id, m/s, printed bool]
            cX, cY, id, speed, printed = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Plastic Box", (cX - 60 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 60 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if (printed != 1):
                if(checkFor2Seconds(speed, cX, cY, "Plastic Box", frameNum)):
                    trackerPlastic.printedObject(id)
                    plastic = DrawLanes(img)
                    plastic = cv2.putText(plastic, ("[%d] pixels/sec" %speed), (cX - 90 , cY + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.imwrite("output/frames%d.jpg" % frameNum, plastic)

    img, StoreLid = DetectLid(img)
    # print(StoreLid)
    obj_ids_lid = trackerLid.update(StoreLid, frameNum)
    if (len(obj_ids_lid) != 0):
        for obj_id in obj_ids_lid:  #obj_id = [x, y, id, m/s, printed bool]
            cX, cY, id, speed, printed = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Lid", (cX , cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX , cY - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if (printed != 1):
                if(checkFor2Seconds(speed, cX, cY, "Lid", frameNum)):
                    trackerLid.printedObject(id)
                    lid = DrawLanes(img)
                    lid = cv2.putText(lid, ("[%d] pixels/sec" %speed), (cX - 90 , cY + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.imwrite("output/frames%d.jpg" % frameNum, lid)

    img, StoreTetrapak = DetectTetrapak(img)
    obj_ids_tetrapak = trackerTetrapak.update(StoreTetrapak, frameNum)
    if (len(obj_ids_tetrapak) != 0):
        for obj_id in obj_ids_tetrapak:  #obj_id = [x,y, id]
            cX, cY, id, speed, printed = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Tetrapak", (cX - 90 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 90 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if (printed != 1):
                if(checkFor2Seconds(speed, cX, cY, "Tetrapak", frameNum)):
                    trackerTetrapak.printedObject(id)
                    tetrapak = DrawLanes(img)
                    tetrapak = cv2.putText(tetrapak, ("[%d] pixels/sec" %speed), (cX - 90 , cY + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.imwrite("output/frames%d.jpg" % frameNum, tetrapak)
    
    img, StoreRoll = DetectRoll(img)
    obj_ids_roll = trackerRoll.update(StoreRoll, frameNum)
    if (len(obj_ids_roll) != 0):
        for obj_id in obj_ids_roll:  #obj_id = [x,y, id]
            cX, cY, id, speed, printed  = obj_id
            cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(img, "Paper roll", (cX - 60 , cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, ("[%d]" %id), (cX - 60 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if (printed != 1):
                if(checkFor2Seconds(speed, cX, cY, "Roll", frameNum)):
                    trackerRoll.printedObject(id)
                    roll = DrawLanes(img)
                    roll = cv2.putText(roll, ("[%d] pixels/sec" %speed), (cX - 90 , cY + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.imwrite("output/frames%d.jpg" % frameNum, roll)
                    

    img = DrawLanes(img)
    cv2.imshow("Video frame", img)
    frameNum += 1

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows
