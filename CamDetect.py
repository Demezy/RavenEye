from imutils.video import VideoStream  # видеопоток
import argparse  # работа с cmd
import datetime  # для отображения даты
import imutils  # работа с картинкой
import time  # для работы со врменем
import cv2  # само компьютероное зрение

# import numpy as np # на всякий случай

ap = argparse.ArgumentParser()  # обработчик аргументов cmd
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument('-f', '--max-frames', type=int, default=1000, help="after this count program will stop")
args = vars(ap.parse_args())  # переменная для нормальной работы с аргументами

if args.get("video", None) is None:  # работаем как с видеофайлом, так и с видеопотоком
    vs = VideoStream(src=0).start()
    time.sleep(2.0)  # даю подумать

else:
    vs = cv2.VideoCapture(args["video"])

firstFrame = None  # дальнейшее сравнение идет с первым кадром
count = 0  # номер кадра с "вором"

while True:
    frame = vs.read()  # получаю кадр из потока
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"  # можно менять, текст, когда все статично
    if frame is None:
        break  # если пользователь пень и не дал ни камеры, ни видео
    frame = imutils.resize(frame, width=500)  # преобразую картинку
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # для работы нужен моноканал, преобразую
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # размытие по гаусу
    if firstFrame is None:
        firstFrame = gray  # устанавливаю первый кадр, с которым сравниваю
        continue
    frameDelta = cv2.absdiff(firstFrame, gray)  # отличие кадра от исходного
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  # маска для отброса лишнего
    thresh = cv2.dilate(thresh, None, iterations=2)  # немного расширяю границу маски
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)  # контуры
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:  # отсеиваем слишком незначительные изменениями
            continue
        (x, y, w, h) = cv2.boundingRect(c)  # обводим в прямоугольник "нарушителя"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        count = count + 1
        cv2.imwrite("./frames/frame%d.jpg" % count, frame)  # сохраняем картинку "нарушителя
    if count >= args.get('max-frames', 1000):  # ограничиваем колличество картинок,можно сделать умнее,чем отключение
        print(f"{args.get('max-frames', 1000)} frames")
        break
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # изменяю текст на экране
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)  # устнавливаю дату и время
    cv2.imshow("Security Feed", frame)  # вывод картинок
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(27)  # закрывем программу, при нажатии на esc
    if key == 27:
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
