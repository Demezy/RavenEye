from CamDetect import Detector
import time

cam = Detector(gui=False)
for i in range(100):
    path = cam.get_frame()
    time.sleep(0.033)
    print(path)
cam.stop()
