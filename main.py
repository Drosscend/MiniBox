import os
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
    path_photo = "OUTPUT/photo.jpg"
    while True:
        utils.takePhoto(cam, path_photo)
        detect.detect(path_photo, 0)
    # cam.release()

