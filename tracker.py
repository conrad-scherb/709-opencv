from DetectLid import *
from DetectTetrapak import *
from DetectRoll import *
from ObjectTracker import *

frameNum = 2300 #6000 # 0

tracker = ObjectTracker()

while True:
    print("current frame: frames%d.jpg" % frameNum)
    img, StoreRoll = DetectTetrapak("framesTrimmed/frames%d.jpg" % frameNum)
    obj_ids = tracker.update(StoreRoll)
    for obj_id in obj_ids:
        cX, cY, id = obj_id
        cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)
        cv2.putText(img, "Tetrapak", (cX - 90 , cY - 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, ("[%d]" %id), (cX - 90 , cY - 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    # if len(obj_ids) > 0:
    #     print("obj id")
    #     print(obj_ids)

    cv2.imshow("no Lid", img)
    cv2.waitKey(0)
    frameNum += 1

    key = cv2.waitKey(3)
    if key == 27:
        break

cv2.destroyAllWindows
