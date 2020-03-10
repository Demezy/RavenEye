from CamDetect import Detector
import Site
import time

# todo асинхронную отправлялку в бота с настройками
# todo ввести настройки в этом файле
cam = Detector(gui=False)
Site.Camera = cam
Site.app.run()

exit(0)

for i in range(100):
    path = cam.get_frame(save_file=True)[1]
    time.sleep(0.033)
    print(path)
cam.stop()
