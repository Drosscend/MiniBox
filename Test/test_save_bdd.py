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

        # Créer un fichier csv de test
        with open("test.csv", "w") as f:
            f.write("date,occurence,top_left,top_right,bottom_left,bottom_right,classe\n")
            f.write("2022-01-01,1,2,3,4,5,6\n")
            f.write("2022-01-02,7,8,9,10,11,12\n")

    def test_save_bdd(self):
        # Appeler la fonction à tester
        save_utils.save_bdd("test.db", "test_table", "test.csv", False)

        # Vérifier que la base de données a été créée
        self.assertTrue(os.path.exists("test.db"))

        # Vérifier que les données du fichier csv ont été sauvegardées dans la base de données
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("2022-01-01", 1, 2, 3, 4, 5, 6))
        self.assertEqual(rows[1], ("2022-01-02", 7, 8, 9, 10, 11, 12))

    def test_file_not_found(self):
        # Vérifier que la fonction génère une exception lorsque le fichier csv n'existe pas
        with self.assertRaises(FileNotFoundError):
            save_utils.save_bdd("test.db", "test_table", "notfound.csv", False)

    def test_save_csv(self):
        timeStart = time.strftime("%Y%m%d-%H%M%S")
        # faire une sauvegarde avec le paramètre keep_csv à True
        save_utils.save_bdd("test.db", "test_table", "test.csv", True)
        # vérifier que le fichier csv de base n'existe plus
        self.assertFalse(os.path.exists("test.csv"))
        # vérifier qu'un nouveau fichier csv a été créé avec le nom du fichier de base + timeStart
        self.assertTrue(os.path.exists("test_" + timeStart + ".csv"))
        # suppression du fichier csv de test
        os.remove("test_" + timeStart + ".csv")

    def tearDown(self):
        # Supprimer les fichiers de test
        try:
            os.remove("test.db")
            os.remove("test.csv")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
