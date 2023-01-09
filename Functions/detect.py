import logging
import os
import time

import cv2 as cv
import numpy as np
import torch

from Functions import TrackedObjects
from Functions import sort
from Functions import utils

log = logging.getLogger("main")

CSV_FILE = 'OUTPUT/data.csv'

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()

# Initialisation de la librairie Sort pour suivre les personnes détectées
model_sort = sort.Sort()


def generate_csv(current):
    """
    Enregistre les résultats de la détection dans un fichier CSV.

    :param current: liste des identifiants des personnes détectées
    :return: None
    """
    date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

    # verifie que le dosser OUTPUT existe et le crée si ce n'est pas le cas
    if not os.path.exists("OUTPUT"):
        os.makedirs("OUTPUT")

    # Initialisation des compteurs pour chaque direction
    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    # Parcours de la liste des identifiants d'objets
    for obj_id in current:
        obj = tracked_objects.get(obj_id)
        if obj.direction is None:
            continue
        if obj.direction == "top-left":
            top_left += 1
        elif obj.direction == "top-right":
            top_right += 1
        elif obj.direction == "bottom-left":
            bottom_left += 1
        elif obj.direction == "bottom-right":
            bottom_right += 1

    # enregistrement des données dans un fichier csv
    try:
        with open(CSV_FILE, 'a') as f:
            # si le fichier est vide, on écrit l'entête
            if f.tell() == 0:
                f.write("date,occurence,top-left,top-right,bottom-left,bottom-right\n")
            f.write(date + ',' + str(len(current)) + ',' + str(top_left) + ',' + str(top_right) + ',' + str(
                bottom_left) + ',' + str(bottom_right) + '\n')
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))


def show_output(image, current):
    """
    Affiche une image avec des rectangles entourant les objets détectés et en affichant leur identifiant et leur
    direction près de chaque objet.

    :param image: image à afficher
    :param current: liste des identifiants des objets détectés
    :return: None
    """

    # Si aucun objet n'a été détecté
    if not current:
        # Affiche un message à l'écran
        cv.putText(image, "Aucun objet detecte", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        # Pour chaque objet détecté, dessine un rectangle autour de l'objet et affiche son identifiant et sa direction
        for obj_id in current:
            # Récupère les informations sur l'objet
            obj = tracked_objects.get(obj_id)  # Objet suivi
            conf = format(obj.confidence, ".2f")
            x1 = obj.x1
            y1 = obj.y1
            x2 = obj.x2
            y2 = obj.y2
            color = obj.color
            direction = obj.direction

            # Dessine un rectangle autour de l'objet
            cv.rectangle(image, (x1, y1), (x2, y2), color, 2)
            # Affiche l'identifiant et la direction de l'objet près de l'objet
            text = f"{obj_id} - {conf}"
            if direction:
                text += f" - ({direction})"

            cv.putText(image, text, (x1, y1 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # Affiche l'image modifiée à l'écran
    cv.imshow('Video', image)


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
        success, frame = video_capture.read()

        # Si le frame n'a pas pu être récupéré ou si la vidéo est terminée, quitte la boucle
        if not success:
            break

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
            obj_id = int(coords[4])  # Identifiant de l'objet
            conf = results.xyxy[0][j][4]  # Confiance de l'objet
            x1 = int(coords[0])
            y1 = int(coords[1])
            x2 = int(coords[2])
            y2 = int(coords[3])

            current.append(obj_id)

            # Si l'objet n'a pas encore été suivi, c'est un nouvel objet
            found = False
            for tracked_object in tracked_objects.tracked_objects:
                if tracked_object.obj_id == obj_id:
                    found = True
                    tracked_object.update_position(conf, x1, y1, x2, y2)
                    break
            if not found:
                color = utils.random_color(obj_id)
                tracked_objects.add(obj_id, conf, x1, y1, x2, y2, color)
                new_detected = True
                log.debug("Nouvel objet détecté: " + str(obj_id))

        if current:
            log.debug("Nombre d'objets détectés: " + str(len(current)))
            # Suppression des éléments qui ne sont plus détectés par le programme.
            if len(tracked_objects.tracked_objects) > len(current):
                log.debug("Suppression de " + str(len(tracked_objects.tracked_objects) - len(current)) + " objets non détectés")
                for tracked_object in tracked_objects.tracked_objects:
                    if tracked_object.obj_id not in current:
                        tracked_objects.remove(tracked_object.obj_id)
        else:
            log.debug("Aucun objet détecté")

        # Enregistrement des résultats dans un fichier csv si une nouvelle personne est détectée
        if only_new:
            if new_detected:
                generate_csv(current)
        else:
            generate_csv(current)

        # Pause entre chaque détection
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # affichage des images
        if show:
            show_output(frame, current)
            key = cv.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

    video_capture.release()
    cv.destroyAllWindows()
    log.debug("Detection terminée")


def main(source, classes, interval, show, debug, only_new):
    # Initialisation de la caméra
    video_capture = cv.VideoCapture(source)

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la source")
        return

    if show:
        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    # Détection des personnes
    detect(video_capture, classes, interval, show, debug, only_new)
