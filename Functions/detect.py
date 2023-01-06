import os
import logging
import time
import torch
import cv2
import numpy as np
from Functions import utils
from Functions import sort
from Functions import TrackedObjects

log = logging.getLogger("main")

CSV_FILE = 'OUTPUT/data.csv'

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()

# Initialisation de la librairie Sort pour suivre les personnes détectées
model_sort = sort.Sort()


def generate_csv(current, classes):
    """
    Enregistre les résultats de la détection dans un fichier CSV.

    :param current: liste des identifiants des personnes détectées
    :param classes: type de détection (0: personnes, 1: vélos)
    :return: None
    """
    date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    # verifie que le dosser OUTPUT existe et le crée si ce n'est pas le cas
    if not os.path.exists("OUTPUT"):
        os.makedirs("OUTPUT")

    # enregistrement des données dans un fichier csv
    try:
        with open(CSV_FILE, 'a') as f:
            # si le fichier est vide, on écrit l'entête
            if f.tell() == 0:
                f.write("date,occurence,type\n")
            f.write(date + ',' + str(len(current)) + ',' + str(classes) + '\r')
    except IOError as e:
        log.error("Erreur lors de l'écriture dans le fichier CSV: " + str(e))


def show_output(image, current):
    """
    Affiche une image avec des rectangles entourant les objets détectés et en affichant leur identifiant et leur direction près de chaque objet.
    :param image: image à afficher
    :param current: liste des identifiants des objets détectés
    :return: None
    """

    # Pour chaque objet détecté, dessine un rectangle autour de l'objet et affiche son identifiant et sa direction
    for name_idx in current:
        # Récupère les informations sur l'objet
        obj = tracked_objects.get(name_idx)  # Objet suivi
        x1 = obj.x1
        y1 = obj.y1
        x2 = obj.x2
        y2 = obj.y2
        color = obj.color  # Coordonnées et couleur de l'objet
        direction = obj.direction  # Direction de l'objet

        # Dessine un rectangle autour de l'objet
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        # Affiche l'identifiant et la direction de l'objet près de l'objet
        text = f"{name_idx} ({direction})" if direction else str(name_idx)
        cv2.putText(image, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Affiche l'image modifiée à l'écran
    cv2.imshow('Video', image)




def detect(video_capture, classes, interval, show, debug, only_new):
    """
    Fonction de détection

    :param video_capture: objet cv2.VideoCapture pour la caméra
    :param classes: type de détection (0: personnes, 1: vélos) ou liste de types
    :param interval: intervalle de temps entre chaque détection
    :param show: affichage de la détection (True/False) (optionnel)
    :param debug: affichage des logs de débug (True/False) (optionnel)
    :param only_new: enregistre uniquement les nouvelles personnes détectées (True/False) (optionnel)
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

        # Pour vérifier que le modèle YOLOv5 est chargé et fonctionne correctement
        try:
            results = model(frame)
        except Exception as e:
            log.error("Erreur lors du traitement de l'image avec le modèle YOLOv5: " + str(e))
            continue

        # Utilisation de la librairie Sort pour suivre les personnes détectées
        detections = np.array(results.xyxy[0][:, :4])

        # Pour vérifier que la bibliothèque de suivi d'objets Sort fonctionne correctement
        try:
            track = model_sort.update(detections)
        except Exception as e:
            log.error("Erreur lors du suivi des objets avec la bibliothèque Sort: " + str(e))
            continue

        # Détection des nouvelles personnes
        current = []
        new_detected = False
        for j in range(len(track.tolist())):
            # Récupère les informations sur l'objet
            coords = track.tolist()[j]
            name_idx = int(coords[4])  # Identifiant de l'objet
            x1 = int(coords[0])
            y1 = int(coords[1])
            x2 = int(coords[2])
            y2 = int(coords[3])

            current.append(name_idx)

        # Si l'objet n'a pas encore été suivi, c'est un nouvel objet
        found = False
        for tracked_object in tracked_objects.tracked_objects:
            if tracked_object.name_idx == name_idx:
                found = True
                tracked_object.update_position(x1, y1, x2, y2)
                break
        if not found:
            color = utils.random_color(name_idx)
            tracked_objects.add(name_idx, x1, y1, x2, y2, color)
            new_detected = True
            log.debug("Nouvel objet détecté: " + str(name_idx))

        log.debug("Objets détectés: " + str(current))

        # Enregistrement des résultats dans un fichier csv si une nouvelle personne est détectée
        if only_new:
            if new_detected:
                generate_csv(current, classes)
        else:
            generate_csv(current, classes)

        # Pause entre chaque détection
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # affichage des images
        if show:
            show_output(frame, current)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

    video_capture.release()
    cv2.destroyAllWindows()
    log.debug("Detection terminée")


def main(webcam, classes, interval, show, debug, only_new):
    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(webcam)

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la webcam")
        return

    if show:
        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    # Détection des personnes
    detect(video_capture, classes, interval, show, debug, only_new)
