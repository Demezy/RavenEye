from imutils.video import VideoStream  # видеопоток
import datetime  # для отображения даты
import imutils  # работа с картинкой
import time  # для работы со врменем
import cv2  # само компьютероное зрение


class Detector:
    def __init__(self, video_src=0, width=640, height=480, fps=20, path='./data/frames/'):
        self.vs = VideoStream(src=video_src).start()
        time.sleep(1.0)  # даю подумать
        print('start service')
        self.count = 0  # номер кадра с "вором"
        self.is_occupied = False
        self.min_area = 500
        self.max_area = 30000
        self.path = path
        self.width = width
        self.height = height

        frame = self.vs.read()
        frame = imutils.resize(frame, width=width, height=height)
        self.source_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # дальнейшее сравнение идет с исходным кадром
        self.get_frame()

        # для трансляции
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*'H264')
        # self.out = cv2.VideoWriter('output.avi', self.fourcc, self.fps, (self.width, self.height), True)

    def change_parameters(self, min_area=False, max_area=False, path=False, width=False, height=False, fps=False):
        if min_area:
            self.min_area = min_area
        if path:
            self.path = path
        if width:
            self.width = width
        if height:
            self.height = height
        if fps:
            self.fps = fps
        if max_area:
            self.max_area = max_area
        self.refresh()
        self.source_frame = self.gray.copy()
        # self.out = cv2.VideoWriter('output.avi', self.fourcc, self.fps, (self.width, self.height), True)

    def get_frame(self, save_file=True) -> (bool, str):
        self.refresh()
        self.detect(save_file=save_file)
        path = self.output(save_file=save_file)
        yield self.is_occupied, path

    def get_frame_obj(self):
        self.frames = open("stream.jpg", 'wb+')
        cv2.imwrite("stream.jpg", self.frame)  # поток для сайта
        yield self.frames.read()

    def refresh(self):
        self.frame = self.vs.read()  # получаю кадр из потока
        self.frame = imutils.resize(self.frame, width=self.width, height=self.height)  # преобразую картинку
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # для работы нужен моноканал, преобразую
        self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)  # размытие по гаусу, убераем шумы
        self.frame_delta = cv2.absdiff(self.source_frame, self.gray)  # отличие кадра от исходного
        self.thresh = cv2.threshold(self.frame_delta, 25, 255, cv2.THRESH_BINARY)[1]  # маска для отброса лишнего
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)  # немного расширяю границу маски

    def detect(self, save_file=True):
        self.is_occupied = False
        cnts = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # контуры
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            if cv2.contourArea(c) < self.min_area:  # отсеиваем слишком незначительные изменениями
                continue
            elif cv2.contourArea(c) > self.max_area:
                self.change_parameters()
            (x, y, w, h) = cv2.boundingRect(c)  # обводим в прямоугольник "нарушителя"
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.is_occupied = True
        if save_file and self.is_occupied:
            self.count += 1

    def output(self, save_file=True):
        text = 'Occupeied' if self.is_occupied else 'Unoccupied'
        cv2.putText(self.frame, f"Status: {text}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)  # изменяю текст на экране
        cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                    1)  # устнавливаю дату и время

        if save_file and self.is_occupied:
            cv2.imwrite(f"{self.path}/frame-{self.count}.jpg", self.frame)  # сохраняем картинку "нарушителя"
        return f"{self.path}/frame-{self.count}.jpg"

    def __del__(self):
        # self.out.release()
        self.vs.stop()
        cv2.destroyAllWindows()
        print('stop service')

    def stop(self):
        self.__del__()


if __name__ == '__main__':
    cam = Detector()
    for i in range(10):
        cam.get_frame()
    cam.stop()
# exit(0)
#
# if self.frame is None:
#
# key = cv2.waitKey(27)  # закрывем программу, при нажатии на esc
# if key == 27:
#     print(111)
