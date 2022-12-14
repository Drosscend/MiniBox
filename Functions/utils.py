import logging
import os
import cv2

log = logging.getLogger("main")


def removeFile(path_to_file_to_remove):
    """
    Supprime le fichier photo.txt
    """
    log.debug("Suppression du fichier" + path_to_file_to_remove)
    if os.path.exists(path_to_file_to_remove):
        os.remove(path_to_file_to_remove)
        log.debug("Fichier " + path_to_file_to_remove + " supprimé")
    else:
        log.error("Fichier " + path_to_file_to_remove + " inexistant")


def takePhoto(cam):
    """
    Prend une photo et la sauvegarde dans le dossier OUTPUT
    """
    log.debug("Prise de photo")
    s, img = cam.read()
    # vérifie si le dossier OUTPUT existe, si non, le crée
    if not os.path.exists("OUTPUT"):
        log.error("Dossier OUTPUT inexistant, création du dossier")
        os.makedirs("OUTPUT")
        log.debug("Dossier OUTPUT créé")
    if s:
        cv2.imwrite("OUTPUT/photo.jpg", img)
        log.debug("Photo prise")
    else:
        log.error("Photo non prise")
