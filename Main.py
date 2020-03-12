from CamDetect import Detector
import Site
import threading
import time

# import argparse

# ap = argparse.ArgumentParser()  # обработчик аргументов cmd
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# ap.add_argument('-f', '--max-frames', type=int, default=1000,
#                 help="after this count program will stop")  # 0 для бесконечного цикла
# ap.add_argument('-p', '--path', default='./frames/', help='dir for frames')  # где хранить файлы
# ap.add_argument('-d', '--delay', type=int, help='delay between message sending in telegram')
# args = vars(ap.parse_args())  # переменная для нормальной работы с аргументами



fps = 20


def main() -> None:
    print('start main')
    c = 0
    while True:
        c = (c + 1) % 10
        time.sleep(1 / fps)
        frame, is_occupied, path = cam.get_frame()
        if c == 0:
            cam.change_parameters()
            print('path', path)
        if False:
            break


cam = Detector(fps=fps)
Site.Camera = cam
Site.fps = fps

main_tread = threading.Thread(target=main, name='main_thread')
site_tread = threading.Thread(target=Site.app.run,
                              kwargs={'host': '127.0.0.1', 'port': '5000', 'ssl_context': ('data/cert.pem', 'data/key.pem')},
                              name="Site")

main_tread.start()
site_tread.start()

main_tread.join()
site_tread.join()
