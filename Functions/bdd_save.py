import csv
import logging
import os
import sqlite3
import time

log = logging.getLogger("main")


def save_bdd(bdd_name: str, table_name: str, csv_file: str) -> None:
    """
    Sauvegarde les données du fichier csv dans la base de données SQLite
    @param bdd_name: nom du fichier de la base de données
    @param table_name: nom de la table
    @param csv_file: nom du fichier csv
    """

    log.info("Sauvegarde des données dans la base de données")

    # calcul du temps d'execution
    start_time = time.time()

    # vérification de l'existence du fichier csv à la racine du projet
    if not os.path.exists(csv_file):
        log.error("Le fichier csv n'existe pas")
        return

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


if __name__ == "__main__":
    save_bdd("detect_save.db", "detect", "OUTPUT/data.csv")
