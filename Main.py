from CamDetect import Detector
import Bot
import Site
import threading
import time
import argparse

ap = argparse.ArgumentParser()  # обработчик аргументов cmd
ap.add_argument('-v', '--video-src', default=0, help='Number of camera')
ap.add_argument("--min-area", type=int, default=500, help="Minimum area size")
ap.add_argument("--max-area", type=int, default=25000, help="Maximum area size")
ap.add_argument('-p', '--path', default='./data/frames/', help='Directory for saving frames')
ap.add_argument('-d', '--delay', type=int, default=1, help='Delay between message sending in telegram')
ap.add_argument('--fps', type=int, default=20, help='Fps on translation')
ap.add_argument('--height', type=int, default=480, help='Image height')
ap.add_argument('--width', type=int, default=640, help='Image width')
args = vars(ap.parse_args())  # переменная для нормальной работы с аргументами

fps = args['fps']
cam = Detector(video_src=args['video_src'], path=args['path'], fps=fps, height=args['height'],
               width=args['width'])
cam.change_parameters(min_area=args['min_area'], max_area=args['max_area'])
Site.Camera = cam
Site.fps = fps


# Функция для отправки в бота
def main() -> None:
    print('start main')
    refresh = 0
    last_send = time.time()
    while True:
        if Bot.stop_for <= 0:
            is_occupied, path = cam.get_frame(save_file=True)
            if is_occupied:
                if last_send - time.time() >= Bot.delay:
                    Bot.send_image(path)
                    last_send = time.time()
                    # print(path)
            # Периодическое обновление исходного кадра
            refresh = (refresh + 1) % 100
            if refresh == 0:
                cam.change_parameters()
        else:
            now = time.time()
            Bot.stop_for -= now - Bot.stop_from
            Bot.stop_from = now


# Создаю и запускаю потоки
main_thread = threading.Thread(target=main, name='main_thread')
site_thread = threading.Thread(target=Site.app.run,
                               kwargs={'host': '127.0.0.1', 'port': '5000',
                                       'ssl_context': ('data/cert.pem', 'data/key.pem')},
                               name="Site")
bot_thread = threading.Thread(target=Bot.main, name='bot_thread')
# Запускаю потоки

main_thread.start()
site_thread.start()
bot_thread.start()

# Корректно завершаю потоки
bot_thread.join()
main_thread.join()
site_thread.join()
