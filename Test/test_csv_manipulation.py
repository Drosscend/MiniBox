import os
import shutil
import unittest
from datetime import datetime

from Functions import TrackedObjects
from Functions import csv_manipulation


class TestGenerateCSV(unittest.TestCase):
    csv_folder_name = 'csv_folder'
    csv_file_name = 'detections.csv'

    def setUp(self):
        # Initialisation des objets suivis
        self.tracked_objects = TrackedObjects.TrackedObjects()
        self.tracked_objects.add(1, 50, 50, 100, 100, 0, (0, 0, 0))
        self.tracked_objects.add(2, 50, 50, 100, 100, 0, (0, 0, 0))
        self.tracked_objects.add(3, 50, 50, 100, 100, 0, (0, 0, 0))
        self.tracked_objects.add(4, 50, 50, 100, 100, 0, (0, 0, 0))

        # Création des objets à ajouter au fichier CSV
        obj1 = self.tracked_objects.get(1)
        obj1.direction = "top-left"
        obj2 = self.tracked_objects.get(2)
        obj2.direction = "top-right"
        obj3 = self.tracked_objects.get(3)
        obj3.direction = "bottom-left"
        obj4 = self.tracked_objects.get(4)
        obj4.direction = "bottom-right"

        current = [1, 2, 3, 4]
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        csv_manipulation.generate_csv(current, self.tracked_objects, self.csv_folder_name, self.csv_file_name)

    def test_createFolder(self):
        self.assertTrue(os.path.isdir(self.csv_folder_name))

    def test_createFile(self):
        self.assertTrue(os.path.isfile(self.csv_folder_name + '/' + self.csv_file_name))

    def test_writeFileHeader(self):
        with open(self.csv_folder_name + '/' + self.csv_file_name, 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines[0], "date,occurence,top-left,top-right,bottom-left,bottom-right,classe\n")

    def test_writeFileContent(self):
        with open(self.csv_folder_name + '/' + self.csv_file_name, 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines[1], self.date + ",4,1,1,1,1,0\n")
            self.assertEqual(len(lines), 2)

    def test_writeFileContent2(self):
        # vider le fichier
        open(self.csv_folder_name + '/' + self.csv_file_name, 'w').close()
        new_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_tracking = TrackedObjects.TrackedObjects()
        new_tracking.add(1, 50, 50, 100, 100, 1, (0, 0, 0))
        new_tracking.add(2, 50, 50, 100, 100, 1, (0, 0, 0))
        new_tracking.add(3, 50, 50, 100, 100, 0, (0, 0, 0))
        new_tracking.add(4, 50, 50, 100, 100, 0, (0, 0, 0))
        new_tracking.add(5, 50, 50, 100, 100, 1, (0, 0, 0))

        obj1 = new_tracking.get(1)
        obj1.direction = "top-left"
        obj2 = new_tracking.get(2)
        obj2.direction = "top-right"
        obj3 = new_tracking.get(3)
        obj3.direction = "bottom-left"
        obj4 = new_tracking.get(4)
        obj4.direction = "bottom-right"
        obj5 = new_tracking.get(5)
        obj5.direction = "top-left"

        current = [1, 2, 3, 4, 5]
        csv_manipulation.generate_csv(current, new_tracking, self.csv_folder_name, self.csv_file_name)
        with open(self.csv_folder_name + '/' + self.csv_file_name, 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines[1], new_date + ",3,2,1,0,0,1\n")
            self.assertEqual(lines[2], new_date + ",2,0,0,1,1,0\n")
            self.assertEqual(len(lines), 3)

    def tearDown(self):
        # Suppression du dossier créé pour les tests
        shutil.rmtree(self.csv_folder_name)


if __name__ == "__main__":
    unittest.main()
