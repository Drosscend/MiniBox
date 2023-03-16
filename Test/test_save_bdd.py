import logging
import os
import sqlite3
import time
import unittest

from Functions import save_utils


class TestSaveBDD(unittest.TestCase):
    def setUp(self):
        # Configurer le logger pour afficher les messages de debug
        logging.basicConfig(level=logging.DEBUG)

        self.csv_folder_name = "test_folder"
        self.csv_file_name = "test_file.csv"
        self.yolov5Params = {
            "output_folder" : self.csv_folder_name,
            "csv_name" : self.csv_file_name,
        }
        self.bddParams = {
            "bdd_name" : "test_table.db",
            "table_name" : "test_table",
            "keep_csv" : False,
        }

        # Créer un fichier csv de test
        path = os.path.join(self.csv_folder_name, self.csv_file_name)
        # créer le dossier si il n'existe pas
        if not os.path.exists(self.csv_folder_name):
            os.makedirs(self.csv_folder_name)
        with open(path, "w") as f:
            f.write("date,occurence,top_left,top_right,bottom_left,bottom_right,classe\n")
            f.write("2022-01-01,1,2,3,4,5,6\n")
            f.write("2022-01-02,7,8,9,10,11,12\n")

    def test_save_bdd(self):
        # Appeler la fonction à tester
        save_utils.save_bdd(self.bddParams, self.yolov5Params)

        # Vérifier que la base de données a été créée
        self.assertTrue(os.path.exists(self.bddParams["bdd_name"]))

        # Vérifier que les données du fichier csv ont été sauvegardées dans la base de données
        conn = sqlite3.connect(self.bddParams["bdd_name"])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("2022-01-01", 1, 2, 3, 4, 5, 6))
        self.assertEqual(rows[1], ("2022-01-02", 7, 8, 9, 10, 11, 12))

    def test_file_not_found(self):
        # Vérifier que la fonction génère une exception lorsque le fichier csv n'existe pas
        self.yolov5Params["csv_name"] = "file_not_found.csv"
        with self.assertRaises(FileNotFoundError):
            save_utils.save_bdd(self.bddParams, self.yolov5Params)

    def test_save_csv(self):
        timeStart = time.strftime("%Y%m%d-%H%M%S")
        # faire une sauvegarde avec le paramètre keep_csv à True
        self.bddParams["keep_csv"] = True
        save_utils.save_bdd(self.bddParams, self.yolov5Params)
        # vérifier que le fichier csv de base n'existe plus
        self.assertFalse(os.path.exists(os.path.join(self.csv_folder_name, self.csv_file_name)))
        # vérifier qu'un nouveau fichier csv a été créé avec le nom du fichier de base + timeStart
        self.assertTrue(os.path.exists(os.path.join(self.csv_folder_name, self.csv_file_name.replace(".csv", "_" + timeStart + ".csv"))))
        # suppression du fichier csv de test
        os.remove(os.path.join(self.csv_folder_name, self.csv_file_name.replace(".csv", "_" + timeStart + ".csv")))

    def tearDown(self):
        # Supprimer les fichiers de test
        try:
            os.remove(self.bddParams["bdd_name"])
            os.remove(self.yolov5Params["output_folder"] + "/" + self.yolov5Params["csv_name"])
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
