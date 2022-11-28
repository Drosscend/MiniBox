import logging
import os
import time
import cv2

log = logging.getLogger("main")


def removeFile(path_to_remove):
    """
    Supprime le fichier photo.txt
    """
    log.debug("Suppression du fichier" + path_to_remove)
    if os.path.exists(path_to_remove):
        os.remove(path_to_remove)
        log.debug("Fichier supprimé")
    else:
        log.debug("Fichier inexistant")


def addTime(path_to_copy, path_to_paste):
    """
    Ajoute l'heure dans le fichier txt
    """
    log.debug("Ajout de l'heure dans le fichier txt")

    # s'il n'y a pas de dossier ou de fichier en créé un
    if not os.path.exists(path_to_paste):
        os.makedirs(os.path.dirname(path_to_paste), exist_ok=True)
        open(path_to_paste, 'a').close()

    if os.stat(path_to_copy).st_size != 0:
        with open(path_to_copy, "r+") as f:
            with open(path_to_paste, "a") as f1:
                for line in f:
                    f1.write(time.strftime("%D %H:%M:%S") + ", " + line)
        log.debug("Heure ajoutée")
    else:
        log.debug("Aucune heure ajoutée")


def takePhoto(cam):
    """
    Prend une photo et la sauvegarde dans le dossier OUTPUT
    """
    log.debug("Prise de photo")
    s, img = cam.read()
    cv2.imwrite("OUTPUT/photo.jpg", img)
    log.debug("Photo prise")