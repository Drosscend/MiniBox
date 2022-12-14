import logging
from CustomFormatter import CustomFormatter
from Functions import utils
from Functions import detect
import cv2

log = logging.getLogger("main")
log.setLevel('DEBUG')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        ret, frame = cam.read()
        detect.detect(frame, 0)
    # cam.release()
