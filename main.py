import os
import time
import logging
from CustomFormatter import CustomFormatter
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


def takePhoto():
    """
    Prend une photo et la sauvegarde dans le dossier OUTPUT
    """
    log.debug("Prise de photo")
    s, img = cam.read()
    cv2.imwrite("OUTPUT/photo.jpg", img)
    log.debug("Photo prise")


def addTime():
    """
    Ajoute l'heure dans le fichier txt
    """
    log.debug("Ajout de l'heure dans le fichier txt")
    path = "OUTPUT/files/labels/photo.txt"

    # s'il n'y a pas de dossier ou de fichier en créé un
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()

    # ajoute l'heure dans le fichier en début de la dernière ligne si le fichier n'est pas vide et que la ligne
    # commence par 0 ou 1

    if os.stat(path).st_size != 0:
        with open(path, "r+") as f:
            lines = f.readlines()
            if lines[-1].startswith("0 ") or lines[-1].startswith("1 "):
                lines[-1] = time.strftime("%H:%M:%S") + " " + lines[-1]
                f.seek(0)
                f.writelines(lines)
                log.debug("Heure ajoutée")
            else:
                log.debug("Aucune heure ajoutée")
    else:
        log.debug("Aucune heure ajoutée")


if __name__ == "__main__":
    # take a photo every 2 seconds
    cam = cv2.VideoCapture(0)
    while True:
        takePhoto()
        detect()
        addTime()
        time.sleep(2)
    cam.release()
