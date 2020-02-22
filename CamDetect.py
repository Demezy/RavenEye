from imutils.video import VideoStream  # видеопоток
import datetime  # для отображения даты
import imutils  # работа с картинкой
import time  # для работы со врменем
import cv2  # само компьютероное зрение


class Detector:
    def __init__(self, video_src=0, gui=True):
        self.vs = VideoStream(src=video_src).start()
        time.sleep(2.0)  # даю подумать
        print('start service')
        self.refresh()
        self.source_frame = self.gray  # дальнейшее сравнение идет с исходным кадром
        self.count = 0  # номер кадра с "вором"
        self.text = "Unoccupied"
        self.min_area = 500
        self.max_area = 30000
        self.gui = gui
        self.path = './frames/'

    def change_parameters(self, min_area=False, max_area=False, path=False):
        if min_area:
            self.min_area = min_area
        if max_area:
            self.max_area = max_area
        if path:
            self.path = path

    def get_frame(self):
            pass

    def self_check(self):
        pass

    def refresh(self):
        self.frame = self.vs.read()  # получаю кадр из потока
        self.frame = imutils.resize(self.frame, width=500)  # преобразую картинку
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # для работы нужен моноканал, преобразую
        self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)  # размытие по гаусу, убераем шумы
        self.frame_delta = cv2.absdiff(self.source_frame, self.gray)  # отличие кадра от исходного
        self.thresh = cv2.threshold(self.frame_delta, 25, 255, cv2.THRESH_BINARY)[1]  # маска для отброса лишнего
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)  # немного расширяю границу маски

    def detect(self):
        cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # контуры
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) < self.max_area:  # отсеиваем слишком незначительные изменениями
                continue
            elif cv2.contourArea(c) > self.max_area:  # калибровка при выключении света
                self.source_frame = self.gray
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # обводим в прямоугольник "нарушителя"
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.text = "Occupied"
            self.count = self.count + 1

    def output(self):
        cv2.putText(self.frame, f"Status: {self.text}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # изменяю текст на экране
        cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),
                    1)  # устнавливаю дату и время
        cv2.imwrite(f"{self.path}/frame-{self.count}.jpg", self.frame)  # сохраняем картинку "нарушителя
        return f"{self.path}/frame-{self.count}.jpg", self.frame

    def stop(self):
        self.vs.stop()
        cv2.destroyAllWindows()


if self.frame is None:
    break  # если пользователь пень и не дал ни камеры, ни видео

#
# if text == 'Occupied' and count % args.get('send_frame', 10) == 0:  # избавляемся от спама в боте
#     # print(path(f"./{args.get('path', './frames/')}/frame-{count}.jpg"))
#     send_image(path(f"./{args.get('path', './frames/')}/frame-{count}.jpg"))
#
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
        cv2.imshow("Frame Delta", frame_delta)

key = cv2.waitKey(27)  # закрывем программу, при нажатии на esc
if key == 27:
    print(111)
