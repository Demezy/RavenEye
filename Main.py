from CamDetect import Detector
import time

# todo асинхронную отправлялку в бота с настройками
# todo ввести настройки в этом файле
cam = Detector(gui=False)
for i in range(100):
    path = cam.get_frame()[1]
    time.sleep(0.033)
    print(path)
cam.stop()
