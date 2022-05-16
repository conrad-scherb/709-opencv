import cv2
import os

# Converts the conveyor feed video into a series of frames and saves them to ~/frames
def FrameExtractor(path):
    os.makedirs("framesTrimmed", exist_ok=True)    # Creates folder ~/framesTrimmed if not preexisting
    # os.makedirs("frames", exist_ok=True)    # Creates folder ~/frames if not preexisting
    
    video = cv2.VideoCapture(path)
    frameNum = 0
    success = 1

    while success:
        success, image = video.read()
        try:
            y1=450
            y2=880
            x1=780
            x2=1780
            roi = image[y1:y2, x1:x2]   #trim video to save computing power

            #pickup point will be at
            #x=233, y to be determined by lanes later :)
            
            cv2.imwrite("framesTrimmed/frames%d.jpg" % frameNum, roi)
            # cv2.imwrite("frames/frames%d.jpg" % frameNum, image)
            frameNum += 1
            print("Processing frame ", frameNum)
        except:
            print("Frame " + str(frameNum) + " empty or nonexistant.")


if __name__ == '__main__':
    FrameExtractor("conveyor_feed.mp4")
    print("Frame processing complete.")
