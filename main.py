import logging
from CustomFormatter import CustomFormatter
from Functions import detect
import cv2

log = logging.getLogger("main")
log.setLevel('DEBUG')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


if __name__ == "__main__":
    detect.detect(0, True)