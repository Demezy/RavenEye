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
        frame = self.vs.read()
        frame = imutils.resize(frame, width=500)
        self.source_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.refresh()
        self.count = 0  # номер кадра с "вором"
        self.is_occupied = False
        self.min_area = 500
        self.gui = gui
        self.path = './frames/'

    def change_parameters(self, min_area=False, path=False):
        if min_area:
            self.min_area = min_area
        if path:
            self.path = path

    def get_frame(self):
        self.refresh()
        self.source_frame = self.gray  # дальнейшее сравнение идет с исходным кадром
        self.detect()
        return self.output()

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
        self.is_occupied = False
        cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # контуры
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) < self.min_area:  # отсеиваем слишком незначительные изменениями
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # обводим в прямоугольник "нарушителя"
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.is_occupied = True
        self.count += 1

    def output(self):
        text = 'Occupeied' if self.is_occupied else 'Unoccupied'
        cv2.putText(self.frame, f"Status: {text}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # изменяю текст на экране
        cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),
                    1)  # устнавливаю дату и время
        cv2.imwrite(f"{self.path}/frame-{self.count}.jpg", self.frame)  # сохраняем картинку "нарушителя"
        if self.gui:
            cv2.imshow("Security Feed", self.frame)  # вывод картинок
            cv2.imshow("Thresh", self.thresh)
            cv2.imshow("Frame Delta", self.frame_delta)
        return f"{self.path}/frame-{self.count}.jpg"

    def stop(self):
        self.vs.stop()
        cv2.destroyAllWindows()
        print('stop service')


if __name__ == '__main__':
    cam = Detector()
    print(cam.get_frame())
    time.sleep(4)
    cam.stop()
# exit(0)
#
# if self.frame is None:
#
# key = cv2.waitKey(27)  # закрывем программу, при нажатии на esc
# if key == 27:
#     print(111)
