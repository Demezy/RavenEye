from CamDetect import Detector
import Site
import threading
import time
import Bot

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
        c = (c + 1) % 100
        time.sleep(1 / fps)
        frame, is_occupied, path = cam.get_frame(save_file=True)
        if c == 0:
            cam.change_parameters()
        if is_occupied:
            Bot.send_image(path)
            print('path', path)
        if False:
            break


cam = Detector(fps=fps)
Site.Camera = cam
Site.fps = fps

main_thread = threading.Thread(target=main, name='main_thread')
site_thread = threading.Thread(target=Site.app.run,
                               kwargs={'host': '127.0.0.1', 'port': '5000',
                                       'ssl_context': ('data/cert.pem', 'data/key.pem')},
                               name="Site")
bot_thread = threading.Thread(target=Bot.main, name='bot_thread')

main_thread.start()
site_thread.start()
bot_thread.start()

bot_thread.join()
main_thread.join()
site_thread.join()
