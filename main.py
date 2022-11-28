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

    pathToCopy = "OUTPUT/files/labels/photo.txt"
    path = "OUTPUT/data.csv"

    # s'il n'y a pas de dossier ou de fichier en créé un
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'a').close()

    if os.stat(pathToCopy).st_size != 0:
        with open(pathToCopy, "r+") as f:
            with open(path, "a") as f1:
                for line in f:
                    f1.write(time.strftime("%D %H:%M:%S") + ", " + line)
        log.debug("Heure ajoutée")
    else:
        log.debug("Aucune heure ajoutée")


def removeFile():
    """
    Supprime le fichier photo.txt
    """
    log.debug("Suppression du fichier photo.txt")
    path = "OUTPUT/files/labels/photo.txt"
    if os.path.exists(path):
        os.remove(path)
        log.debug("Fichier supprimé")
    else:
        log.debug("Fichier inexistant")


if __name__ == "__main__":
    # take a photo every 2 seconds
    cam = cv2.VideoCapture(0)
    while True:
        takePhoto()
        removeFile()
        detect()
        addTime()
    cam.release()
