import logging
import time

import cv2
import yolov5

from Functions import csv_manipulation
from Functions import cv2_manipulation
from Functions import TrackedObjects
from Functions import sort
from Functions import utils

log = logging.getLogger("main")

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()


def detect(video_capture: cv2.VideoCapture, object_types: list[int], interval: float, display_detection: bool,
           yolov5_paramms: dict) -> None:
    """
    Détection des objets
    @param video_capture: Flux vidéo
    @param object_types: Liste des types d'objets à détecter
    @param interval: Intervalle de temps entre chaque détection
    @param display_detection: Affichage des boites englobantes
    @param yolov5_paramms: Paramètres de la librairie Yolov5
    """

    log.info("Début de la détection")
    # load pretrained model
    model = yolov5.load(yolov5_paramms["weights"])
    model.classes = object_types
    model.conf = yolov5_paramms["conf_thres"]  # NMS confidence threshold
    model.iou = yolov5_paramms["iou_thres"]  # NMS IoU threshold
    model.agnostic = yolov5_paramms["agnostic_nms"]  # NMS class-agnostic
    model.multi_label = yolov5_paramms["multi_label_nms"]  # NMS multiple labels per box
    model.max_det = yolov5_paramms["max_det"]  # maximum number of detections per image
    model.amp = yolov5_paramms["amp"]  # Automatic Mixed Precision (AMP) inference

    output_folder = yolov5_paramms["output_folder"]
    csv_name = yolov5_paramms["csv_name"]

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
            object_x1 = int(tracked_object[0])
            object_y1 = int(tracked_object[1])
            object_x2 = int(tracked_object[2])
            object_y2 = int(tracked_object[3])
            object_id = int(tracked_object[4])
            object_conf = float(tracked_object[5])
            object_classe = int(tracked_object[6])

            current.append(object_id)

            # Si l'objet n'a pas encore été suivi, c'est un nouvel objet
            found = False
            for tracked_object in tracked_objects.tracked_objects:
                if tracked_object.obj_id == object_id:
                    found = True
                    tracked_object.update_position(object_conf, object_x1, object_y1, object_x2, object_y2)
                    break
            if not found:
                color = utils.get_random_color(object_id)
                tracked_objects.add(object_id, object_conf, object_x1, object_y1, object_x2, object_y2, object_classe,
                                    color)
                log.debug("Nouvel objet détecté: {}".format(object_id))

        # Supprime les objets qui n'ont pas été détectés dans le frame courant
        for tracked_object in tracked_objects.tracked_objects:
            if tracked_object.obj_id not in current:
                tracked_objects.remove(tracked_object.obj_id)
                log.debug("Suppression de l'objet: {}".format(tracked_object.obj_id))

        # Pause entre chaque détection si spécifiée
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # Génération du fichier CSV
        CSV_manipulation.generate_csv(current, tracked_objects, output_folder, csv_name)

        # affichage des images si spécifié
        if display_detection:
            CV2_manipulation.draw_bounding_boxes(frame, current, tracked_objects)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

    video_capture.release()
    cv2.destroyAllWindows()
    log.info("Detection terminée")


def main(source: int, classes: list[int], interval: float, display_detection: bool, yolov5_paramms: dict) -> None:
    """
    Fonction principale
    @param source: Source de la vidéo
    @param classes: Liste des types d'objets à détecter
    @param interval: Intervalle de temps entre chaque détection
    @param display_detection: Affichage des boites englobantes
    @param yolov5_paramms: Paramètres de la librairie Yolov5
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
        detect(video_capture, classes, interval, display_detection, yolov5_paramms)
    except Exception as e:
        log.error("Erreur lors de la détection: {}".format(e))
