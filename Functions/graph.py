import csv
import matplotlib.pyplot as plt
import time


def createGraph(path):
    """
    Crée un graphique à partir d'un fichier csv
    Les occurences seront sur l'axe des ordonnées et les dates sur l'axe des abscisses
    """
    # ouvrir le fichier csv
    with open(path, 'r'):
        reader = csv.DictReader(open(path, 'r'), delimiter=',')
        # créer une liste avec les occurences
        date = []
        occurence = []
        for row in reader:
            date.append(time.strftime("%H:%M:%S", time.strptime(row['date'], "%d/%m/%Y %H:%M:%S")))
            occurence.append(int(row['occurence']))
        plt.plot(date, occurence)
        plt.xlabel('Date')
        plt.ylabel('Occurence')
        plt.title('Graphique des occurences par date')
        plt.show()


if __name__ == "__main__":
    createGraph("OUTPUT/data.csv")
