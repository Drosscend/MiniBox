import os
import shutil
import unittest
from datetime import datetime

from Functions import TrackedObjects
from Functions import save_utils


class TestSaveCsv(unittest.TestCase):
    def setUp(self):
        self.list_of_directions = {0: {
            "total": 5,
            "top-left": 2,
            "top-right": 1,
            "bottom-left": 1,
            "bottom-right": 1
        }}
        self.classe = 0
        self.csv_folder_name = "test_folder"
        self.csv_file_name = "test_file.csv"
        self.params = {
            "output_folder" : self.csv_folder_name,
            "csv_name" : self.csv_file_name,
        }
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        save_utils.save_csv(self.list_of_directions, self.params)

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
            self.assertEqual(lines[1], self.date + ",5,2,1,1,1,0\n")

    def tearDown(self):
        # Suppression du dossier créé pour les tests
        shutil.rmtree(self.csv_folder_name)


if __name__ == "__main__":
    unittest.main()
