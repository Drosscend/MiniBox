import logging
import time
import torch
import cv2
import os
import numpy as np
from Functions import utils
from Functions.sort import Sort

log = logging.getLogger("main")

# Dictionnaire pour stocker les identifiants des personnes suivies
tracked_object = {}

# Initialisation de la librairie Sort pour suivre les personnes détectées
model_sort = Sort()


def detect(webcam, classes, show=False, debug=False):
    """
    Fonction de détection
    :param webcam: webcam à utiliser
    :param classes: type de détection (0: personnes, 1: vélos) ou liste de types
    :param show: affichage de la détection (True/False) (optionnel)
    :param debug: affichage des logs de débug (True/False) (optionnel)
    :return: None
    Enregistre les résultats dans un fichier csv avec comme entête:
    date,occurence,type,positions
    """
    log.debug("Début de la détection")
    cam = cv2.VideoCapture(webcam)
    if show:
        log.warning("Affichage des résultats activé, pour fermer la fenêtre, appuyez sur la touche 'q'")

    while cam.isOpened():
        _, frame = cam.read()
        # création du model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', verbose=debug)

        # paramètres du model
        model.classes = classes
        model.conf = 0.25  # NMS confidence threshold
        model.iou = 0.45  # NMS IoU threshold
        model.agnostic = False  # NMS class-agnostic
        model.multi_label = True  # NMS multiple labels per box
        model.max_det = 20  # maximum number of detections per image
        model.amp = True  # Automatic Mixed Precision (AMP) inference

        # detection
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

    cam.release()
    cv2.destroyAllWindows()
    log.debug("Detection terminée")


def generate_csv(occurence, classes):
    log.debug("------------------------------------------")
    log.debug("Traitement des résultats")
    # Si au moins une personne a été détectée, on enregistre les résultats dans le fichier CSV
    if occurence > 0:
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
    log.debug("Résultats traités")
    log.debug("------------------------------------------")


def show_output(image, track):
    for i in range(len(track.tolist())):
        coords = track.tolist()[i]
        name_idx = int(coords[4])
        x1 = int(coords[0])
        y1 = int(coords[1])
        x2 = int(coords[2])
        y2 = int(coords[3])
        color = utils.random_color(name_idx)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, str(name_idx), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    cv2.imshow('YOLO', image)
