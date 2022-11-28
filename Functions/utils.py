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
        log.debug("Fichier " + path_to_remove + " supprimé")
    else:
        log.error("Fichier " + path_to_remove + " inexistant")


def addTime(path_to_copy, path_to_paste):
    """
    Ajoute l'heure dans le fichier txt
    """
    log.debug("Ajout de l'heure dans le fichier txt")

    # s'il n'y a pas de dossier ou de fichier en créé un et rajouter en-tête : date, type, position
    if not os.path.exists(path_to_paste):
        os.makedirs(os.path.dirname(path_to_paste), exist_ok=True)
        open(path_to_paste, 'a').close()

    # si le fichier path_to_paste n'existe pas ou et vide on le crée avec une en-tête
    if os.stat(path_to_paste).st_size == 0:
        with open(path_to_paste, "w") as f:
            f.write("date,occurence,type\n")

    # regrouper les lignes du fichier txt en une ligne en rajoutant en seconde position le nombre d'occurence
    if os.stat(path_to_copy).st_size != 0:
        with open(path_to_copy, "r+") as f:
            with open(path_to_paste, "a") as f1:
                occurence = len(f.readlines())
                f.seek(0)
                # récupérer la première ligne du fichier copy
                line = f.readline()
                # récupérer la date
                date = time.strftime("%d/%m/%Y %H:%M:%S")
                # récupérer le type
                type = line.split(" ")[0]
                # TODO récupérer la position
                # écrire dans le fichier paste
                f1.write(f"{date},{occurence},{type}\n")
        log.debug("Heure ajoutée")
    else:
        log.error("Aucune heure ajoutée")


def takePhoto(cam):
    """
    Prend une photo et la sauvegarde dans le dossier OUTPUT
    """
    log.debug("Prise de photo")
    s, img = cam.read()
    if s:
        cv2.imwrite("OUTPUT/photo.jpg", img)
        log.debug("Photo prise")
    else:
        log.error("Photo non prise")

"""
date,type,position
11/28/22 18:30:28,0,0.570312 0.602083 0.615625 0.791667
11/28/22 18:30:33,0,0.546875 0.628125 0.571875 0.73125

"""


def csvToJson(path):
    """
    Create a json with the csv file
    """
    log.debug("Création du fichier json")
    import csv
    import json
    with open(path, 'r'):
        reader = csv.DictReader(open(path, 'r'), delimiter=',')
        out = json.dumps([row for row in reader])
        with open('OUTPUT/data.json', 'w') as f:
            f.write(out)
    log.debug("Fichier json créé")
