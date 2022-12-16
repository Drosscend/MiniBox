import logging
import time
import torch
import cv2
import os
import numpy as np
from Functions import utils
from Functions import sort

log = logging.getLogger("main")

# Dictionnaire pour stocker les identifiants des personnes suivies
tracked_object = {}

# Initialisation de la librairie Sort pour suivre les personnes détectées
model_sort = sort.Sort()


def detect(video_capture, classes, interval=10, show=False, debug=False):
    """
    Fonction de détection
    Enregistre les résultats dans un fichier csv avec comme entête:
    date,occurence,type,positions

    :param video_capture: objet cv2.VideoCapture pour la caméra
    :param classes: type de détection (0: personnes, 1: vélos) ou liste de types
    :param interval: intervalle de temps entre chaque détection
    :param show: affichage de la détection (True/False) (optionnel)
    :param debug: affichage des logs de débug (True/False) (optionnel)
    :return: None
    """
    log.debug("Début de la détection")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', verbose=debug)
    model.classes = classes
    model.conf = 0.25
    model.iou = 0.45
    model.agnostic = False
    model.multi_label = True
    model.max_det = 20
    model.amp = True
    while video_capture.isOpened():
        _, frame = video_capture.read()

        results = model(frame)

        # Utilisation de la librairie Sort pour suivre les personnes détectées
        detections = np.array(results.xyxy[0][:, :4])

        # Si aucune personne n'est détectée, on passe à l'image suivante
        if len(detections) == 0:
            continue

        track = model_sort.update(detections)

        # Détection des nouvelles personnes
        new_object_count = 0
        for j in range(len(track.tolist())):
            coords = track.tolist()[j]
            name_idx = int(coords[4])
            # Si l'identifiant de la personne n'est pas déjà enregistré, c'est une nouvelle personne
            if name_idx not in tracked_object:
                new_object_count += 1
                tracked_object[name_idx] = 1

        generate_csv(new_object_count, classes)

        # affichage des images
        if show:
            show_output(frame, track)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        # Pause entre chaque détection
        log.debug("Pause de " + str(interval) + " secondes")
        time.sleep(interval)

    video_capture.release()
    cv2.destroyAllWindows()
    log.debug("Detection terminée")


def generate_csv(occurence, classes):
    """
    Enregistre les résultats de la détection dans un fichier CSV.

    :param occurence: nombre de personnes ou vélos détectés
    :param classes: type de détection (0: personnes, 1: vélos)
    :return: None
    """
    # Si au moins une personne a été détectée, on enregistre les résultats dans le fichier CSV
    if occurence > 0:
        log.debug("Nouvelle objet détecté " + str(occurence) + " fois" + " de type " + str(classes))

        date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        # verifie que le dosser OUTPUT existe et le crée si ce n'est pas le cas
        if not os.path.exists("OUTPUT"):
            os.makedirs("OUTPUT")
        # enregistrement des données dans un fichier csv
        with open('OUTPUT/data.csv', 'a') as f:
            # si le fichier est vide, on écrit l'entête
            if f.tell() == 0:
                f.write("date,occurence,type\n")
            f.write(date + ',' + str(occurence) + ',' + str(classes) + '\r')


def show_output(image, track):
    """
    Affiche une image avec des rectangles entourant les personnes détectées et en affichant leur identifiant près de chaque personne.

    :param image: image à afficher
    :param track: informations sur les personnes détectées, y compris leurs coordonnées et leur identifiant
    :return: None
    """

    # Pour chaque personne détectée, dessine un rectangle autour de la personne et affiche son identifiant
    for i in range(len(track.tolist())):
        # Récupère les informations sur la personne
        coords = track.tolist()[i]
        name_idx = int(coords[4])  # Identifiant de la personne
        x1 = int(coords[0])
        y1 = int(coords[1])
        x2 = int(coords[2])
        y2 = int(coords[3])
        # Génère une couleur aléatoire pour chaque personne en utilisant son identifiant
        color = utils.random_color(name_idx)
        # Dessine un rectangle autour de la personne
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        # Affiche l'identifiant de la personne près de la personne
        cv2.putText(image, str(name_idx), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Affiche l'image modifiée à l'écran
    cv2.imshow('YOLO', image)


def main(webcam, classes, interval, show, debug):
    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(webcam)

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la webcam")
        exit()

    # Détection des personnes
    detect(video_capture, classes, interval, show, debug)
