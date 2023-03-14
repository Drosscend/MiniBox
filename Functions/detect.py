import logging
import os
import platform
import time
from typing import List, Optional, Union

import cv2
import numpy as np
import supervision as sv
import torch
from norfair import Tracker

from Functions import TrackedObjects
from Functions import save_utils
from Functions import utils

log = logging.getLogger("main")


class YOLO:
    def __init__(self, model_name: str, device: str, verbose: bool):
        """
        @param model_name: Nom du modèle à charger
        @param device: Device sur lequel le modèle doit être chargé
        @param verbose: Afficher les informations de chargement du modèle
        """
        # Vérification de la disponibilité de CUDA si nécessaire
        if device != "cpu":
            if not torch.cuda.is_available():
                log.error("Vous avez demandé un device CUDA, mais il n'est pas disponible")
                raise Exception("Vous avez demandé un device CUDA, mais il n'est pas disponible")

        # Chargement du modèle
        self.model = torch.hub.load("ultralytics/yolov5", model_name, device=device, verbose=verbose)

    def __call__(self, img: Union[str, np.ndarray], conf_threshold: float = 0.25,
                 iou_threshold: float = 0.45, image_size: int = 720, agnostic: bool = False, multi_label: bool = True,
                 max_det: int = 50, amp: bool = True, classes: Optional[List[int]] = None) -> torch.tensor:
        """
        @param img: Image à traiter
        @param conf_threshold: Seuil de confiance
        @param iou_threshold: Seuil d'intersection sur union
        @param image_size: Taille de l'image
        @param agnostic: NMS class-agnostic
        @param multi_label: NMS multiple labels per box
        @param max_det: Maximum number of detections per image
        @param amp: Automatic Mixed Precision (AMP) inference
        @param classes: Classes à détecter
        @return: Résultats de la détection
        """
        self.model.conf = conf_threshold
        self.model.iou = iou_threshold
        self.model.agnostic = agnostic  # NMS class-agnostic
        self.model.multi_label = multi_label  # NMS multiple labels per box
        self.model.max_det = max_det  # maximum number of detections per image
        self.model.amp = amp  # Automatic Mixed Precision (AMP) inference

        if classes is not None:
            self.model.classes = classes
        detections = self.model(img, size=image_size)
        return detections


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
    model = YOLO(yolov5_paramms["weights"], yolov5_paramms["device"], base_params["debug"])

    # Initialisation de la collection d'objets suivis
    tracked_objects_informations = TrackedObjects.TrackedObjects()

    interval = base_params["interval"]

    display_fps = base_params["display_fps"]
    if display_fps:
        prev_frame_time = 0

    display_detection = base_params["display_detection"]
    if display_detection:
        if platform.system() == 'Linux' and not os.getenv('DISPLAY', ''):
            cv2.namedWindow("Minibox", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        else:
            cv2.namedWindow("Minibox", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Minibox", 640, 480)

        log.info("Pour quitter l'application, appuyez sur la touche 'q'")

    output_folder = yolov5_paramms["output_folder"]
    csv_name = yolov5_paramms["csv_name"]

    tracker = Tracker(distance_function="iou", distance_threshold=0.7)

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

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
                image_size=640,
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
            object_x1 = int(tracked_object.last_detection.points[0][0])
            object_y1 = int(tracked_object.last_detection.points[0][1])
            object_x2 = int(tracked_object.last_detection.points[1][0])
            object_y2 = int(tracked_object.last_detection.points[1][1])
            object_id = int(tracked_object.id)
            object_classe = int(tracked_object.label)

            currents_id.append(object_id)

            # Si l'objet n'a pas encore été suivi, c'est un nouvel objet
            found = False
            for obj in tracked_objects_informations.tracked_objects:
                if obj.obj_id == object_id:
                    found = True
                    obj.update_position(object_x1, object_y1, object_x2, object_y2)
                    break
            if not found:
                color = utils.get_random_color(object_id)
                tracked_objects_informations.add(object_id, object_x1, object_y1, object_x2, object_y2,
                                                 object_classe, color)
                log.debug("Nouvel objet détecté: {}".format(object_id))

        # Supprime les objets qui n'ont pas été détectés dans le frame courant
        for tracked_object in tracked_objects_informations.tracked_objects:
            if tracked_object.obj_id not in currents_id:
                tracked_objects_informations.remove(tracked_object.obj_id)
                log.debug("Objet supprimé: {}".format(tracked_object.obj_id))

        # Génération du fichier CSV
        if base_params["save_in_csv"]:
            save_utils.save_csv(currents_id, tracked_objects_informations, output_folder, csv_name)

        # sauvegarde dans la base de données
        if bdd_params["save_in_bdd"]:
            if bdd_params["time_to_save"] == time.strftime("%H:%M:%S"):
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

    try:
        detect(video_capture, base_params, yolov5_paramms, bdd_params)
    except Exception as e:
        log.error("Erreur lors de la détection: {}".format(e))
