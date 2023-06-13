import csv
import logging
import os
import sqlite3
import time
from datetime import datetime
from typing import Any

log = logging.getLogger("main")


def save_bdd(bdd_params: dict, yolov5_paramms: dict) -> None:
    """
    Sauvegarde les données du fichier csv dans la base de données SQLite
    @param bdd_params: dictionnaire contenant les paramètres de la base de données
    @param yolov5_paramms: dictionnaire contenant les paramètres de YOLOv5
    """

    log.info("Sauvegarde des données dans la base de données")

    bdd_name = bdd_params["bdd_name"]
    table_name = bdd_params["table_name"]
    output_folder = yolov5_paramms["output_folder"]
    csv_name = yolov5_paramms["csv_name"]
    csv_file = os.path.join(output_folder, csv_name)
    keep_csv = bdd_params["keep_csv"]

    # calcul du temps d'execution
    start_time = time.time()

    # vérification de l'existence du fichier csv à la racine du projet
    if not os.path.exists(csv_file):
        log.error("Le fichier csv n'existe pas")
        raise FileNotFoundError("Le fichier csv n'existe pas")

    # Connexion à la base de données
    conn = sqlite3.connect(bdd_name)
    cursor = conn.cursor()

    # Création de la table
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ("
                       f"date TEXT, "
                       f"occurrence INTEGER, "
                       f"top_left INTEGER, "
                       f"top_right INTEGER, "
                       f"bottom_left INTEGER, "
                       f"bottom_right INTEGER, "
                       f"classe INTEGER)")
    except sqlite3.OperationalError as e:
        log.error("Erreur lors de la création de la table: {}".format(e))
        return

    # Ouverture du fichier csv
    try:
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cursor.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)", row)
    except FileNotFoundError as e:
        log.error("Erreur lors de l'ouverture du fichier csv: {}".format(e))
        return

    # Sauvegarde des modifications
    conn.commit()
    conn.close()

    # suppression du fichier csv
    if keep_csv:
        # renommage du fichier csv pour éviter de le réutiliser (nom + date)
        try:
            log.debug("Renommage du fichier csv")
            os.rename(csv_file, (csv_file[:-4] + "_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"))
        except FileNotFoundError as e:
            log.error("Erreur lors du renommage du fichier csv: {}".format(e))
            return
    try:
        log.debug("Suppression du fichier csv")
        os.remove(csv_file)
    except FileNotFoundError as e:
        log.error("Erreur lors de la suppression du fichier csv: {}".format(e))
        return

    # Affichage du temps d'execution
    log.info(f"Temps d'execution : {(time.time() - start_time).__round__(2)} secondes")

    # attendre 1 seconde pour éviter de sauvegarder plusieurs fois dans la base de données
    time.sleep(1)
    log.info("Sauvegarde terminée")


def save_csv(list_of_directions: dict[Any, dict[str, int]], yolov5_paramms) -> None:
    """
    Génère un fichier CSV contenant le nombre d'occurrence total et par direction
    @param list_of_directions: Liste des directions des objets détectés par classe
    @param csv_folder_name: Nom du dossier dans lequel enregistrer le fichier CSV
    @param csv_file_name: Nom du fichier CSV
    """
    csv_folder_name = yolov5_paramms["output_folder"]
    csv_file_name = yolov5_paramms["csv_name"]
    # verifie que le dosser csv_folder_name existe et le crée si ce n'est pas le cas
    if not os.path.exists(csv_folder_name):
        log.info("Création du dossier {}".format(csv_folder_name))
        os.makedirs(csv_folder_name)

    # récupération de la date au format international et UTC
    datestring = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # enregistrement des données dans un fichier csv
    try:
        path = os.path.join(csv_folder_name, csv_file_name)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            # si le fichier est vide, on écrit l'entête
            if os.path.getsize(path) == 0:
                writer.writerow(["date", "occurrence", "top-left", "top-right", "bottom-left", "bottom-right", "classe"])
            for classe, infos in list_of_directions.items():
                writer.writerow([
                    datestring,
                    infos["total"],
                    infos["top-left"],
                    infos["top-right"],
                    infos["bottom-left"],
                    infos["bottom-right"],
                    classe
                ])
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))
