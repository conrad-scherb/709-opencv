import math

class ObjectTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        #disappeared frames count
        self.disappeared = {}
        self.maxDisappeared = 5


    def update(self, objectsCOM):
        # Objects boxes and ids
        # print(objectsCOM)
        objects_bbs_ids = []

        print(objects_bbs_ids)
        #if no objects detected
        if len(objectsCOM) == 0 and len(objects_bbs_ids) != 0:
            print("hold up")
            
            print("")

        # Get center point of new object
        for obj in objectsCOM:
            cx, cy = obj

            # Find out if that object was detected already, by comparing current object (cx,cy) against each stored object 1 by 1 (id, (pt.cx, pt.cy))
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([cx, cy, id])
                    same_object_detected = True
                    break

            # REGISTER: New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([cx, cy, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDs not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



