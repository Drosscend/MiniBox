import logging
import os
import random
import time
import csv
from datetime import datetime

import cv2
import torch

from Functions import TrackedObjects
from Functions import sort

log = logging.getLogger("main")

CSV_FILE_NAME = 'OUTPUT/data.csv'

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()


def generate_csv(current):
    """Enregistre les résultat de la détection dans un fichier CSV.

    Args:
        current (list): Liste des identifiants des personnes détectées
    """


    # verifie que le dosser OUTPUT existe et le crée si ce n'est pas le cas
    if not os.path.exists("OUTPUT"):
        os.makedirs("OUTPUT")

    date = datetime.now()

    # Initialisation des compteurs pour chaque direction
    counts = {
        "top-left": 0,
        "top-right": 0,
        "bottom-left": 0,
        "bottom-right": 0
    }

    # Parcours de la liste des identifiants d'objets
    for obj_id in current:
        obj = tracked_objects.get(obj_id)
        if obj is not None:
            # Incrémentation du compteur de la direction de l'objet s'il existe
            if obj.direction is not None:
                counts[obj.direction] += 1

    # enregistrement des données dans un fichier csv
    try:
        with open(CSV_FILE_NAME, 'a', newline='') as f:
            writer = csv.writer(f)
            # si le fichier est vide, on écrit l'entête
            if os.path.getsize(CSV_FILE_NAME) == 0:
                writer.writerow(["date", "occurence", "top-left", "top-right", "bottom-left", "bottom-right"])
            writer.writerow([date.strftime("%d/%m/%Y %H:%M:%S"), len(current), counts["top-left"], counts["top-right"],
                             counts["bottom-left"], counts["bottom-right"]])
    except IOError as e:
        log.warning("Erreur lors de l'écriture dans le fichier CSV: " + str(e))


def draw_bounding_boxes(image, objects):
    """Dessine des boîtes englobantes autour des objets détectés et affiche leurs ID, leurs confidence et leurs directions

    Args:
        image (frame): Image à afficher
        objects (list): Liste des objets détectés
    """

    # Si aucun objet n'a été détecté
    if not objects:
        cv2.putText(image, "Aucun objet detecte", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for object_id in objects:
            object_info = tracked_objects.get(object_id)
            if object_info is not None:
                confidence = format(object_info.confidence, ".2f")
                x1 = object_info.x1
                y1 = object_info.y1
                x2 = object_info.x2
                y2 = object_info.y2
                color = object_info.color
                direction = object_info.direction

                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                text = f"{object_id} - {confidence}"
                if direction:
                    text += f" - ({direction})"

                cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Video", image)


def get_random_color(name_idx):
    """Génère une couleur aléatoire pour chaque personne

    Args:
        name_idx (int): Identifiant de la personne

    Returns:
        tuple: tuple contenant les valeurs RGB de la couleur
    """
    random.seed(name_idx)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def detect(video_capture, object_types, interval, display_detection):
    """Fonction de détection

    Args:
        video_capture (VideoCapture): Objet VideoCapture pour la caméra
        object_types (int): type de détection (0: personnes, 1: vélos, ...)
        interval (float): intervalle de temps entre chaque détection
        display_detection (bool): affichage de la détection (True/False) (optionnel)

    Raises:
        ValueError: Type d'objet non valide
        ValueError: Interval non valide
        ValueError: Affichage de la détection non valide
    """

    # Vérifier si les paramètres ont des valeurs valides
    if not isinstance(object_types, int) or object_types < 0:
        raise ValueError(f"Type d'objet non valide: {object_types}")
    if not isinstance(interval, float) or interval < 0:
        raise ValueError("Intervalle non valide")
    if not isinstance(display_detection, bool):
        raise ValueError("Affichage de la détection non valide")

    log.info("Début de la détection")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.classes = object_types
    model.conf = 0.25
    model.iou = 0.45
    model.agnostic = False
    model.multi_label = True
    model.max_det = 20
    model.amp = True

    # Initialisation de la librairie Sort pour suivre les personnes détectées
    model_sort = sort.Sort()

    while video_capture.isOpened():
        success, frame = video_capture.read()

        # Si le frame n'a pas pu être récupéré ou si la vidéo est terminée, quitte la boucle
        if not success:
            break

        # Pour vérifier que le modèle YOLOv5 est chargé et fonctionne correctement
        try:
            results = model(frame)
        except Exception as e:
            log.error("Erreur lors du traitement de l'image avec le modèle YOLOv5: {}".format(e))
            continue

        predictions = results.pred[0]

        try:
            # Utilisation de la librairie Sort pour suivre les personnes détectées
            track = model_sort.update(predictions)
        except Exception as e:
            log.error("Erreur lors du suivie des objets: {}".format(e))
            continue

        # Enregistre les objets détectés
        current = []
        for j in range(len(track.tolist())):
            # Récupère les informations sur l'objet
            tracked_object = track.tolist()[j]
            object_id = int(tracked_object[4])
            object_conf = results.xyxy[0][j][4]
            object_x1 = int(tracked_object[0])
            object_y1 = int(tracked_object[1])
            object_x2 = int(tracked_object[2])
            object_y2 = int(tracked_object[3])

            current.append(object_id)

            # Si l'objet n'a pas encore été suivi, c'est un nouvel objet
            found = False
            for tracked_object in tracked_objects.tracked_objects:
                if tracked_object.obj_id == object_id:
                    found = True
                    tracked_object.update_position(object_conf, object_x1, object_y1, object_x2, object_y2)
                    break
            if not found:
                color = get_random_color(object_id)
                tracked_objects.add(object_id, object_conf, object_x1, object_y1, object_x2, object_y2, color)
                log.debug("Nouvel objet détecté: {}".format(object_id))

        # Supprime les objets qui n'ont pas été détectés dans le frame courant
        for tracked_object in tracked_objects.tracked_objects:
            if tracked_object.obj_id not in current:
                tracked_objects.remove(tracked_object.obj_id)
                log.debug("Suppression de l'objet: {}".format(tracked_object.obj_id))

        # affichage des images si spécifié
        if display_detection:
            draw_bounding_boxes(frame, current)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

        # Génération du fichier CSV
        generate_csv(current)

        # Pause entre chaque détection si spécifiée
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

    video_capture.release()
    cv2.destroyAllWindows()
    log.info("Detection terminée")


def main(source, classes, interval, display_detection):
    """fonction principale de l'application

    Args:
        source (int): id de la caméra
        classes (int): type de détection (0: personnes, 1: vélos, ...)
        interval (float): intervalle de temps entre chaque détection
        display_detection (bool): affichage de la détection (True/False) (optionnel)
    """
    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(source)

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la source, verifier le fichier de configuration")
        return

    if display_detection:
        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    # Détection des personnes
    try:
        detect(video_capture, classes, interval, display_detection)
    except ValueError as e:
        log.error("Erreur lors de la détection: {}".format(e))
    except Exception as e:
        log.error("Erreur lors de la détection: {}".format(e))
