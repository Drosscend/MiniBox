import csv
import logging
import os
import sqlite3
import time
from datetime import datetime

log = logging.getLogger("main")

from Functions import TrackedObjects


def save_bdd(bdd_name: str, table_name: str, csv_file: str, keep_csv: bool) -> None:
    """
    Sauvegarde les données du fichier csv dans la base de données SQLite
    @param bdd_name: nom du fichier de la base de données
    @param table_name: nom de la table
    @param csv_file: nom du fichier csv
    @param keep_csv: booléen pour garder ou non le fichier csv
    """

    log.info("Sauvegarde des données dans la base de données")

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
                       f"occurence INTEGER, "
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


def save_csv(current: list[int], tracked_objects: TrackedObjects.TrackedObjects, csv_folder_name: str,
             csv_file_name: str) -> None:
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
    counts_classe = {}
    counts_direction_classe = {}

    # Parcours de la liste des identifiants d'objets
    for obj_id in current:
        obj = tracked_objects.get(obj_id)
        if obj is not None:
            # incrémentation du compteur de la classe de l'objet s'il existe
            if obj.classe in counts_classe:
                counts_classe[obj.classe] += 1
            else:
                counts_classe[obj.classe] = 1
            # Si la classe n'est pas encore dans le dictionnaire de compteurs de direction par classe, on l'ajoute
            if obj.classe not in counts_direction_classe:
                counts_direction_classe[obj.classe] = {
                    "top-left": 0,
                    "top-right": 0,
                    "bottom-left": 0,
                    "bottom-right": 0
                }
            # Incrémente le compteur de direction pour cette classe
            if obj.direction is not None:
                counts_direction_classe[obj.classe][obj.direction] += 1

    # enregistrement des données dans un fichier csv
    try:
        path = os.path.join(csv_folder_name, csv_file_name)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            # si le fichier est vide, on écrit l'entête
            if os.path.getsize(path) == 0:
                writer.writerow(["date", "occurence", "top-left", "top-right", "bottom-left", "bottom-right", "classe"])
            for classe, nb_occurence in counts_classe.items():
                writer.writerow([
                    date.strftime("%d/%m/%Y %H:%M:%S"),
                    nb_occurence,
                    counts_direction_classe[classe]["top-left"],
                    counts_direction_classe[classe]["top-right"],
                    counts_direction_classe[classe]["bottom-left"],
                    counts_direction_classe[classe]["bottom-right"],
                    classe
                ])
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))
