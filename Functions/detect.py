import logging
import os
import random
import time

import cv2
import torch

from Functions import TrackedObjects
from Functions import sort

log = logging.getLogger("main")

CSV_FILE = 'OUTPUT/data.csv'

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()

def generate_csv(current):
    """
    Enregistre les résultats de la détection dans un fichier CSV.

    :param current: Liste des identifiants des personnes détectées
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
        if obj is not None:
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


def draw_bounding_boxes(image, objects):
    """
    Draws bounding boxes around detected objects and displays their IDs and directions.

    :param image: Image to display
    :param objects: List of detected object IDs
    """

    # Si aucun objet n'a été détecté
    if not objects:
        cv2.putText(image, "No objects detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
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
    """
    Génère une couleur aléatoire pour chaque personne
    :param name_idx: identifiant
    :return: couleur aléatoire
    """
    random.seed(name_idx)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def detect(video_capture, classes, interval, show):
    """
    Fonction de détection

    :param video_capture: Objet VideoCapture pour la caméra
    :param classes: type de détection (0: personnes, 1: vélos) ou liste de types
    :param interval: intervalle de temps entre chaque détection
    :param show: affichage de la détection (True/False) (optionnel)
    :return: None
    """
    log.info("Début de la détection")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.classes = classes
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
            log.error("Erreur lors du traitement de l'image avec le modèle YOLOv5: " + str(e))
            continue

        predictions = results.pred[0]

        try:
            # Utilisation de la librairie Sort pour suivre les personnes détectées
            track = model_sort.update(predictions)
        except Exception as e:
            log.error("Erreur lors du suivie des objets: " + str(e))
            continue

        # Enregistre les objets détectés
        current = []
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
                color = get_random_color(obj_id)
                tracked_objects.add(obj_id, conf, x1, y1, x2, y2, color)
                log.debug("Nouvel objet détecté: " + str(obj_id))

        if current:
            log.debug("Nombre d'objets détectés: " + str(len(current)))
            # Suppression des éléments qui ne sont plus détectés par le programme.
            if len(tracked_objects.tracked_objects) > len(current):
                log.debug("Suppression de " + str(
                    len(tracked_objects.tracked_objects) - len(current)) + " objets non détectés")
                for tracked_object in tracked_objects.tracked_objects:
                    if tracked_object.obj_id not in current:
                        tracked_objects.remove(tracked_object.obj_id)
        else:
            log.debug("Aucun objet détecté")

        # Génération du fichier CSV
        generate_csv(current)

        # Pause entre chaque détection
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # affichage des images
        if show:
            draw_bounding_boxes(frame, current)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

    video_capture.release()
    cv2.destroyAllWindows()
    log.info("Detection terminée")


def main(source, classes, interval, show):
    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(source)

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la source, verifier le fichier de configuration")
        return

    if show:
        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    # Détection des personnes
    detect(video_capture, classes, interval, show)
