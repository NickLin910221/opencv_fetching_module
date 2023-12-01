import cv2
import threading
import os
import time
from threading import Lock

class IPCam:
    __slots__ = ["img", "status", "url", "entrance_name", "source", "nosignal", "fps", "last_frame", "lock"]

    def __init__(self, url, fps) -> None:
        self.url = url
        self.status = False
        self.last_frame = time.time()
        self.fps = fps
        self.img = None
        self.lock = Lock()
        self.source = cv2.VideoCapture(self.url)
        self.nosignal = cv2.imread(os.path.join(os.path.abspath(os.path.dirname(__file__)), f"./no_signal.jpg"))

    def run(self):
        threading.Thread(target=self.fetch, daemon=True, args=()).start()

    def fetch(self):
        while True:
            self.status, img = self.source.read()
            print(f"Status : {self.status}")
            # Reconnect while lost connection
            if not self.status:
                self.source.release()
                time.sleep(1)
                self.source = cv2.VideoCapture(self.url)
                continue
            self.img = cv2.resize(img, [1280, 720], interpolation = cv2.INTER_AREA)
            self.last_frame = time.time()
            time.sleep(1/self.fps)

    def getentrance_name(self):
        return self.entrance_name
    
    def getimg(self):
        if (self.status is not None) and (self.img is not None):
            return self.img.copy(), self.last_frame, True
        elif self.status is False
            return self.nosignal, self.last_frame, False
        else:
            return self.nosignal, self.last_frame, False