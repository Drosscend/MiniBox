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
