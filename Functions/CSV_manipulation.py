import csv
import logging
import os
from datetime import datetime

from Functions import TrackedObjects

log = logging.getLogger("main")


def generate_csv(current: list[int], tracked_objects: TrackedObjects.TrackedObjects, csv_folder_name:str, csv_file_name: str) -> None:
    """
    Génère un fichier CSV contenant les informations des objets détectés
    @param current: Liste des ids des objets détectés à l'instant t
    @param tracked_objects: Liste des objets détectés
    @param csv_folder_name: Nom du dossier dans lequel enregistrer le fichier CSV
    @param csv_file_name: Nom du fichier CSV
    """
    # verifie que le dosser csv_folder_name existe et le crée si ce n'est pas le cas
    if not os.path.exists(csv_folder_name):
        log.info("Création du dossier {}".format(csv_folder_name))
        os.makedirs(csv_folder_name)

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
            # incrémentation du compteur de la classe de l'objet s'il existe
            if obj.classe in counts_classe:
                counts_classe[obj.classe] += 1
            else:
                counts_classe[obj.classe] = 1

    # enregistrement des données dans un fichier csv
    try:
        path = os.path.join(csv_folder_name, csv_file_name)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            # si le fichier est vide, on écrit l'entête
            if os.path.getsize(path) == 0:
                writer.writerow(["date", "occurence", "top-left", "top-right", "bottom-left", "bottom-right", "classe"])
            for classe, nb_occurence in counts_classe.items():
                writer.writerow([date.strftime("%d/%m/%Y %H:%M:%S"), nb_occurence, counts_direction["top-left"],
                                 counts_direction["top-right"],
                                 counts_direction["bottom-left"], counts_direction["bottom-right"], classe])
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))
