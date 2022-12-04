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
            f.write("date,occurence,type,position\n")

    position = []

    # construction du fichier si plusieurs occurence (1 ligne par occurence)
    # 0 0.183594 0.778125 0.235938 0.439583\n
    # 0 0.50625 0.764583 0.496875 0.466667\n
    # la position est donc un tableau contenant toutes les positions ex: [[0.183594, 0.778125, 0.235938, 0.439583], [0.50625, 0.764583, 0.496875, 0.466667]]
    with open(path_to_copy, "r") as f:
        for line in f:
            if line != "\n":
                value = line.split(" ")[2:]
                #suppresion du retour à la ligne
                value[-1] = value[-1].replace("\n", "")
                position.append(value)
            else:
                position.append(line)

    # check if path_to_copy exist
    if os.path.exists(path_to_copy):
        # regrouper les lignes du fichier txt en une ligne en rajoutant en seconde position le nombre d'occurence
        if os.stat(path_to_copy).st_size != 0:
            with open(path_to_copy, "r+") as f:
                with open(path_to_paste, "a") as f1:
                    occurence = len(f.readlines())
                    f.seek(0) # remettre le curseur au début du fichier
                    # récupérer la première ligne du fichier copy
                    line = f.readline()
                    # récupérer la date
                    date = time.strftime("%d/%m/%Y %H:%M:%S")
                    # récupérer le type
                    type = line.split(" ")[0]
                    # écrire dans le fichier paste
                    f1.write(date + "," + str(occurence) + "," + type + "," + str(position) + "\n")
            log.debug("Heure ajoutée")
        else:
            log.error("Aucune heure ajoutée")
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
