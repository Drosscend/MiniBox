import logging
import os
import platform
import time

import cv2
import supervision as sv
from norfair import Tracker

from Functions import TrackedObjects
from Functions import Yolo
from Functions import save_utils
from Functions import utils

log = logging.getLogger("main")


def detect(
        video_capture: cv2.VideoCapture,
        base_params: dict,
        yolov5_paramms: dict,
        bdd_params: dict
) -> None:
    """
    Détection des objets
    @param video_capture: Flux vidéo
    @param base_params: Paramètres de base
    @param yolov5_paramms: Paramètres de la librairie Yolov5.
    @param bdd_params: Paramètres de la base de données
    """
    log.info("Début de la détection")

    # Initialisation du modèle YOLOv5
    try:
        model = Yolo.YOLO(yolov5_paramms["weights"], yolov5_paramms["device"], base_params["debug"])
    except Exception as e:
        log.error("Erreur lors de l'initialisation du modèle YOLOv5: {}".format(e))
        exit(1)

    # Initialisation du tracker
    try:
        tracker = Tracker(distance_function="iou", distance_threshold=0.7)
    except Exception as e:
        log.error("Erreur lors de l'initialisation du tracker: {}".format(e))
        exit(1)

    # Initialisation de la collection d'objets suivis pour caluler la direction et faire l'enregistrement
    tracked_objects_informations = TrackedObjects.TrackedObjects()

    # interval entre chaque détection
    interval = base_params["interval"]

    # Pour afficher le FPS
    display_fps = base_params["display_fps"]
    if display_fps:
        prev_frame_time = 0

    # Pour afficher les détections, si demandé
    display_detection = base_params["display_detection"]
    if display_detection:
        if platform.system() == 'Linux' and not os.getenv('DISPLAY', ''):
            cv2.namedWindow("Minibox", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        else:
            cv2.namedWindow("Minibox", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Minibox", 640, 480)

        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )

        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    # Pour enregistrer les détections, si demandé
    if base_params["save_in_csv"]:
        output_folder = yolov5_paramms["output_folder"]
        csv_name = yolov5_paramms["csv_name"]
        # Initialisation de la liste des positions pour l'enregistrement dans le CSV
        info_for_class = {
            "total": 0,
            "top-left": 0,
            "top-right": 0,
            "bottom-left": 0,
            "bottom-right": 0
        }
        list_of_directions = {}
        for classe in base_params["classes"]:
            list_of_directions[classe] = info_for_class.copy()
        total_all = 0

        # copie de la liste pour la sauvegarde
        list_of_directions_for_save = list_of_directions.copy()

        # Initialisation du temps de la dernière sauvegarde
        last_csv_save = time.time()

    # début de la boucle de détection
    while video_capture.isOpened():
        success, frame = video_capture.read()
        # Si le frame n'a pas pu être récupéré ou si la vidéo est terminée, quitte la boucle
        if not success:
            break

        # Pour vérifier que le modèle YOLOv5 est chargé et fonctionne correctement
        try:
            results = model(
                frame,
                conf_threshold=yolov5_paramms["conf_thres"],
                iou_threshold=yolov5_paramms["iou_thres"],
                classes=base_params["classes"],
                agnostic=yolov5_paramms["agnostic_nms"],
                multi_label=yolov5_paramms["multi_label_nms"],
                max_det=yolov5_paramms["max_det"],
                amp=yolov5_paramms["amp"],
            )
        except Exception as e:
            log.error("Erreur lors du traitement de l'image avec le modèle YOLOv5: {}".format(e))
            continue

        detections = utils.yolo_detections_to_norfair_detections(results)

        try:
            # Utilisation de la librairie Sort pour suivre les personnes détectées
            tracked_objects = tracker.update(detections=detections)
        except Exception as e:
            log.error("Erreur lors du suivie des objets: {}".format(e))
            continue

        # Enregistre les objets détectés
        currents_id = []
        for tracked_object in tracked_objects:
            # Récupère les informations sur l'objet
            (object_x1, object_y1), (object_x2, object_y2) = map(lambda p: (int(p[0]), int(p[1])),
                                                                 tracked_object.last_detection.points)
            object_id = int(tracked_object.id)
            currents_id.append(object_id)

            # Si l'objet est suivi, nous mettons à jour les positions
            found = False
            for obj in tracked_objects_informations.tracked_objects:
                if obj.obj_id == object_id:
                    found = True
                    obj.update_position(object_x1, object_y1, object_x2, object_y2)
                    break

            # Si l'objet n'a pas encore été suivi, nous créons une nouvelle entrée dans la collection
            if not found:
                object_classe = int(tracked_object.label)
                tracked_objects_informations.add(
                    object_id, object_x1, object_y1,
                    object_x2, object_y2, object_classe
                )
                log.debug("Nouvel objet détecté: {}".format(object_id))

        # Supprime les objets qui n'ont pas été détectés dans le frame courant
        for tracked_object in tracked_objects_informations.tracked_objects:
            if tracked_object.obj_id not in currents_id:
                if base_params["save_in_csv"]:
                    # Enregistrement des directions dans l'ojet de la collection pour le CSV
                    classe = tracked_object.classe
                    direction = tracked_object.direction
                    if direction == "top-left":
                        list_of_directions[classe]["top-left"] += 1
                    elif direction == "top-right":
                        list_of_directions[classe]["top-right"] += 1
                    elif direction == "bottom-left":
                        list_of_directions[classe]["bottom-left"] += 1
                    elif direction == "bottom-right":
                        list_of_directions[classe]["bottom-right"] += 1
                    list_of_directions[classe]["total"] += 1
                    total_all += 1
                # Suppression de l'objet de la collection
                tracked_objects_informations.remove(tracked_object.obj_id)
                log.debug("Objet supprimé: {}".format(tracked_object.obj_id))

        # Génération du fichier CSV et de la base de données si demandé
        if base_params["save_in_csv"]:
            # save_utils.save_csv(currents_id, tracked_objects_informations, output_folder, csv_name)
            # enregistrement dans le CSV toutes les 1 minutes
            if time.time() - last_csv_save > 60:
                if total_all == 0:
                    log.debug("Aucune donnée à enregistrer dans le CSV")
                else:
                    log.debug("Enregistrement des données dans le CSV")
                    save_utils.save_csv2(list_of_directions, output_folder, csv_name)
                # réinitialisation des variables pour la sauvegarde
                list_of_directions = list_of_directions_for_save.copy()
                total_all = 0
                last_csv_save = time.time()

            # sauvegarde dans la base de données si demandé
            if bdd_params["save_in_bdd"] and bdd_params["time_to_save"] == time.strftime("%H:%M:%S"):
                csv_pah = os.path.join(output_folder, csv_name)
                save_utils.save_bdd(bdd_params["bdd_name"], bdd_params["table_name"], csv_pah, bdd_params["keep_csv"])

        # Pause entre chaque détection si spécifiée
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # Affichage des images si spécifié
        if display_detection:
            # si pas de détection, affiche un message
            if len(tracked_objects) == 0:
                cv2.putText(frame, "Aucune detection", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                detections = sv.Detections.from_yolov5(results)
                labels = []
                for tracked_object in tracked_objects:
                    current_id = tracked_object.id
                    direction = tracked_objects_informations.get(current_id).direction
                    confidence = format(tracked_object.last_detection.scores[0], ".2f")
                    labels.append(f"id : {current_id} - {direction} - {confidence}")

                frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

            # Affichage des FPS si spécifié
            if display_fps:
                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time
                fps = str(int(fps)) + " FPS"
                cv2.putText(frame, fps, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Minibox", frame)

            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == -1:
                continue

    video_capture.release()
    cv2.destroyAllWindows()

    # si la détection est terminée, mais que list_of_directions n'est pas vide, on enregistre les données restantes
    if base_params["save_in_csv"] and total_all != 0:
        log.debug("Enregistrement des données dans le CSV")
        save_utils.save_csv2(list_of_directions, output_folder, csv_name)

    log.info("Detection terminée")


def main(
        base_params: dict,
        yolov5_paramms: dict,
        bdd_params: dict
) -> None:
    """
    Fonction principale
    @param base_params: Paramètres de base
    @param yolov5_paramms: Paramètres de la librairie Yolov5
    @param bdd_params: Paramètres de la base de données
    """
    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(base_params["source"])

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la source, verifier le fichier de configuration")
        return

    detect(video_capture, base_params, yolov5_paramms, bdd_params)
