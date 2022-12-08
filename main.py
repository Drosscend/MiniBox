import os
import logging
import time

from CustomFormatter import CustomFormatter
from Functions import utils
import cv2

log = logging.getLogger("main")
log.setLevel('DEBUG')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


def detect():
    """
    Lance le script detect.py et détecte la source de l'image
    enregistre les informations de capture dans le fichier OUPUT/files/labels/photo.txt
    """
    log.debug("Début de la détection")

    param = ""
    param += f" --project OUTPUT"
    param += f" --name files"
    param += f" --classes 0"  # 0 = personne, 1 = vélo
    # param += f" --source {source}"
    param += f" --source OUTPUT/photo.jpg"
    param += f" --conf 0.25"
    param += f" --vid-stride 1"
    # param += " --view-img"
    param += " --exist-ok"
    param += " --save-txt"
    # param += " --save-crop"
    param += " --nosave"

    os.system(f"python yolov5/detect.py {param}")
    log.debug("Detection terminée")


if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    path_detect = "OUTPUT/files/labels/photo.txt"
    path_output = "OUTPUT/data.csv"
    path_json = "OUTPUT/data.json"
    path_image = "OUTPUT/photo.jpg"
    while True:
        utils.takePhoto(cam)
        utils.removeFile(path_detect)
        detect()
        utils.removeFile(path_image)
        utils.createCSV(path_detect, path_output)
        # utils.removeFile(path_json)
        # utils.csvToJson(path_output)
    cam.release()

