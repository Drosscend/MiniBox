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


def takePhoto(cam, path_photo):
    """
    Prend une photo et la sauvegarde dans le dossier OUTPUT
    : param cam: caméra
    : param path_photo: chemin de la photo
    """
    log.debug("Prise de photo")
    s, img = cam.read()
    # vérifie si le dossier de path_photo, si non, le crée
    if not os.path.exists(os.path.dirname(path_photo)):
        log.error("Le dossier " + os.path.dirname(path_photo) + " n'existe pas")
        os.makedirs(os.path.dirname(path_photo))
        log.debug("Le dossier " + os.path.dirname(path_photo) + " a été créé")

    if s:
        cv2.imwrite(path_photo, img)
        log.debug("Photo prise")
    else:
        log.error("Photo non prise")
