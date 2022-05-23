import math

class ObjectTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        #store speed (pixels/second) and initial frame obj was detected in
        self.speed = {}
        #disappeared frames count
        self.disappeared = {}
        self.maxDisappeared = 3
        self.printed = {}


    def update(self, objectsCOM, frameNum):
        # Objects boxes and ids
        objects_bbs_ids = []

        # print("input:")
        # print(objectsCOM)
        # print("old")
        # print(self.center_points)
        # print("")
        # print("center points: ")
        # print(self.center_points)
        # print("delete points: ")
        # print(self.disappeared)
        # print("")

        #if no objects detected, but previous contains objects
        if len(objectsCOM) == 0:
            if (len(self.center_points) != 0):
                new_disappeared_count = self.disappeared.copy()
                for id in new_disappeared_count:
                    self.disappeared[id] += 1   # increment disappear COUNT
                    
                    if self.disappeared[id] > self.maxDisappeared:  #if gone for more than 5 frame-reads, remove object
                        # print("center points")
                        # print(self.center_points[id])
                        # print("del count")
                        # print(self.disappeared[id])
                        del self.center_points[id]
                        del self.speed[id]
                        del self.disappeared[id]
                        del self.printed[id]
                for id, pt in self.center_points.items():
                    cx, cy = self.center_points[id]
                    speed = self.speed[id][0]
                    objects_bbs_ids.append([cx, cy, id, speed, self.printed[id]])
            else:
                return []

        # Get center point of new object
        for obj in objectsCOM:
            cx, cy = obj

            # Find out if that object was detected already, by comparing current object (cx,cy) against each stored object 1 by 1 (id, (pt.cx, pt.cy))
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(int(cx) - pt[0], int(cy) - pt[1])

                if (dist < 60) and ((int(cx) - (pt[0])) <= 5): # (minimum distance, and new x is left side) (+10 pixel tolerance)
                    #todo speed 
                    bork = frameNum - self.speed[id][2]
                    velocity = ( (self.speed[id][0] * (bork - (frameNum - self.speed[id][1])) / 30 + (pt[0] - cx)) / ( (frameNum - self.speed[id][2]) / 30) )
                    self.speed[id] = [velocity, frameNum, self.speed[id][2]]
                    self.center_points[id] = (cx, cy)
                    self.disappeared[id] = 0
                    objects_bbs_ids.append([cx, cy, id, velocity, self.printed[id]])
                    same_object_detected = True
                    break

            # REGISTER: New object is detected we assign the ID to that object
            if same_object_detected is False:
                # print("before")
                # print(self.center_points)
                self.center_points[self.id_count] = [cx, cy]
                # print("test2)")
                # print(self.center_points)
                self.speed[self.id_count] = [0, frameNum, frameNum] # [speed = 0, last updated frame = frameNum, first frame = frameNum]
                self.disappeared[self.id_count] = 0
                self.printed[self.id_count] = 0
                objects_bbs_ids.append([cx, cy, self.id_count, 0, self.printed[self.id_count]])
                self.id_count += 1
                
    
        # new_disappeared_count = self.disappeared.copy()
        # for id in new_disappeared_count:
        #     if self.disappeared[id] > self.maxDisappeared:  #if gone for more than 5 frame-reads, remove object
        #         # print("center points")
        #         # print(self.center_points[id])
        #         # print("del count")
        #         # print(self.disappeared[id])
        #         del self.center_points[id]
        #         del self.speed[id]
        #         del self.disappeared[id]

        # Clean the dictionary by center points to remove IDs not used anymore
        new_center_points = {}
        new_disappear_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, object_id, _, _ = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

            count = self.disappeared[object_id]
            new_disappear_points[object_id] = count
            # print(obj_bb_id)
            # print("new")
            # print(new_center_points)

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        self.disappeared = new_disappear_points.copy()
        # print("this is obj id")
        # print(self.center_points)
        # print("")
        # print(self.center_points)
        # print("speed")
        # print(self.speed)
        return objects_bbs_ids

    def printedObject(self, objectID):
        self.printed[objectID] = 1




