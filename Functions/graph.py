import csv
import time

import matplotlib.pyplot as plt


def createGraph(path):
    """
    Crée un graphique à partir d'un fichier csv
    Les occurences seront sur l'axe des ordonnées et les dates sur l'axe des abscisses
    : param path : Chemin du fichier csv
    """
    with open(path, 'r'):
        reader = csv.DictReader(open(path, 'r'), delimiter=',')
        date = []
        occurence = []
        for row in reader:
            date.append(time.strftime("%H:%M:%S", time.strptime(row['date'], "%d/%m/%Y %H:%M:%S")))
            occurence.append(int(row['occurence']))

        plt.plot(date, occurence)
        plt.xlabel('Date')
        plt.ylabel('Occurence')
        plt.title('Graphique des occurences')
        plt.show()


if __name__ == "__main__":
    createGraph("OUTPUT/data.csv")
