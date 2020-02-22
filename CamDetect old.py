"""Этот файл устарел и потом будет удален. Веду рефакторинг."""

from imutils.video import VideoStream  # видеопоток
import argparse  # работа с cmd
import datetime  # для отображения даты
import imutils  # работа с картинкой
import time  # для работы со врменем
import cv2  # само компьютероное зрение
from os.path import abspath as path
import base64
import zmq

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://127.0.0.1:5555')

from telegram_bot / main
import send_image

ap = argparse.ArgumentParser()  # обработчик аргументов cmd
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument('-f', '--max-frames', type=int, default=1000,
                help="after this count program will stop")  # 0 для бесконечного цикла
ap.add_argument('-A', '--max-area', type=int, default=30000, help="number for calibrate")  # experimental parameter
ap.add_argument('-p', '--path', default='./frames/', help='dir for frames')  # где хранить файлы
ap.add_argument('-g', '--gui', type=int, default=0,
                help='enable or disable gui')  # включаем и выключаем отображение окон
ap.add_argument('-s', '--send-frame', type=int, default=10,
                help='Send frame, whose number is divisible for this number')  # зыщита от спама ботом
args = vars(ap.parse_args())  # переменная для нормальной работы с аргументами

if args.get("video", None) is None:  # работаем как с видеофайлом, так и с видеопотоком
    vs = VideoStream(src=0).start()
    time.sleep(2.0)  # даю подумать
else:
    vs = cv2.VideoCapture(args["video"])
print('start service')
sourceFrame = None  # дальнейшее сравнение идет с исходным кадром
count = 0  # номер кадра с "вором"

while True:
    frame = vs.read()  # получаю кадр из потока
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"  # можно менять, текст, когда все статично
    if frame is None:
        break  # если пользователь пень и не дал ни камеры, ни видео
    frame = imutils.resize(frame, width=500)  # преобразую картинку
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # для работы нужен моноканал, преобразую
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # размытие по гаусу, убераем шумы
    if sourceFrame is None:
        sourceFrame = gray  # устанавливаю первый кадр, с которым сравниваю
        continue
    frameDelta = cv2.absdiff(sourceFrame, gray)  # отличие кадра от исходного
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  # маска для отброса лишнего
    thresh = cv2.dilate(thresh, None, iterations=2)  # немного расширяю границу маски
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)  # контуры
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:  # отсеиваем слишком незначительные изменениями
            continue
        elif cv2.contourArea(c) > args.get('max_area', 30000):  # калибровка при выключении света
            sourceFrame = gray
            continue
        (x, y, w, h) = cv2.boundingRect(c)  # обводим в прямоугольник "нарушителя"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        count = count + 1
    cv2.putText(frame, "Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # изменяю текст на экране
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)  # устнавливаю дату и время
    cv2.imwrite(f"{args.get('path', './frames/')}/frame-{count}.jpg", frame)  # сохраняем картинку "нарушителя

    if text == 'Occupied' and count % args.get('send_frame', 10) == 0:  # избавляемся от спама в боте
        # print(path(f"./{args.get('path', './frames/')}/frame-{count}.jpg"))
        send_image(path(f"./{args.get('path', './frames/')}/frame-{count}.jpg"))

    if args.get('max_frames', None) is None and count >= 1000:
        # ограничиваем колличество картинок,можно сделать умнее,чем отключение
        print('1000 frames, stop service')
        break
    else:
        if args["max_frames"] <= count and args["max_frames"] != 0:
            print(f"{args.get('max_frames')} frames, stop service")
            break
    if not (args.get('gui') is None):
        if args['gui']:
            cv2.imshow("Security Feed", frame)  # вывод картинок
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)

    # отправка данных в поток
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)

    key = cv2.waitKey(27)  # закрывем программу, при нажатии на esc
    if key == 27:
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
