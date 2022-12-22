import logging
import os
import random

log = logging.getLogger("main")


def removeFile(path_to_file_to_remove):
    """
    Supprime le fichier passé en paramètre
    :param path_to_file_to_remove: chemin du fichier à supprimer
    """
    log.debug("Suppression du fichier " + path_to_file_to_remove)
    if os.path.exists(path_to_file_to_remove):
        os.remove(path_to_file_to_remove)
        log.debug("Fichier " + path_to_file_to_remove + " supprimé")
    else:
        log.error("Fichier " + path_to_file_to_remove + " inexistant")


def random_color(name_idx):
    """
    Génère une couleur aléatoire pour chaque personne
    :param name_idx: identifiant
    :return: couleur aléatoire
    """
    random.seed(name_idx)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b
