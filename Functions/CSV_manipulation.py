import csv
import os
import logging
from datetime import datetime

from Functions import TrackedObjects

log = logging.getLogger("main")

CSV_FILE_NAME = 'OUTPUT/data.csv'

def generate_csv(current: list[int], tracked_objects: TrackedObjects.TrackedObjects) -> None:
    """
    Génère un fichier CSV contenant les informations des objets détectés
    @param current: Liste des ids des objets détectés à l'instant t
    @param tracked_objects: Liste des objets détectés
    """
    # verifie que le dosser OUTPUT existe et le crée si ce n'est pas le cas
    if not os.path.exists("OUTPUT"):
        os.makedirs("OUTPUT")

    date = datetime.now()

    # Initialisation des compteurs pour chaque direction et classe d'objet
    counts_direction = {
        "top-left": 0,
        "top-right": 0,
        "bottom-left": 0,
        "bottom-right": 0
    }
    counts_classe = {}

    # Parcours de la liste des identifiants d'objets
    for obj_id in current:
        obj = tracked_objects.get(obj_id)
        if obj is not None:
            # Incrémentation du compteur de la direction de l'objet s'il existe
            if obj.direction is not None:
                counts_direction[obj.direction] += 1
            #incrémentation du compteur de la classe de l'objet s'il existe
            if obj.classe in counts_classe:
                counts_classe[obj.classe] += 1
            else :
                counts_classe[obj.classe] = 1

    # enregistrement des données dans un fichier csv
    try:
        with open(CSV_FILE_NAME, 'a', newline='') as f:
            writer = csv.writer(f)
            # si le fichier est vide, on écrit l'entête
            if os.path.getsize(CSV_FILE_NAME) == 0:
                writer.writerow(["date", "occurence", "top-left", "top-right", "bottom-left", "bottom-right", "classe"])
            for classe, nb_occurence in counts_classe.items():
                writer.writerow([date.strftime("%d/%m/%Y %H:%M:%S"), nb_occurence, counts_direction["top-left"], counts_direction["top-right"],
                                 counts_direction["bottom-left"], counts_direction["bottom-right"], classe])
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))