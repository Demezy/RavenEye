from CamDetect import Detector
import Site
import threading
import asyncio

# import argparse

# ap = argparse.ArgumentParser()  # обработчик аргументов cmd
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# ap.add_argument('-f', '--max-frames', type=int, default=1000,
#                 help="after this count program will stop")  # 0 для бесконечного цикла
# ap.add_argument('-p', '--path', default='./frames/', help='dir for frames')  # где хранить файлы
# ap.add_argument('-g', '--gui', type=int, default=0,
#                 help='enable or disable gui')  # включаем и выключаем отображение окон
# ap.add_argument('-d', '--delay', type=int, help='delay between message sending in telegram')
# args = vars(ap.parse_args())  # переменная для нормальной работы с аргументами

# todo асинхронную отправлялку в бота с настройками
# todo ввести настройки в этом файле
cam = Detector(gui=False)


# Site.Camera = cam
# Site.app.run()

# while True:
#     asyncio.sleep(1/20)
#     print(cam.get_frame()[1:])

# threading.Thread(target=Site.app.run).start()


async def frame_worker(sf=False):
    frame, is_occupied, path = cam.get_frame(save_file=sf)
    if is_occupied:
        print('Отправка в бота', path)
    yield frame


async def main():
    threading.Thread(target=Site.app.run).start()
    Site.task = asyncio.create_task(frame_worker())
    fps = 20
    while True:
        await asyncio.sleep(1000 / fps)
        await asyncio.run(frame_worker(sf=True))


if __name__ == '__main__':
    print('test')
    asyncio.run(main())
