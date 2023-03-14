import logging
from typing import List, Optional, Union

import cv2
import numpy as np
import supervision as sv
import torch
from norfair import Detection, Tracker

log = logging.getLogger("main")
import time

MAX_DISTANCE: int = 10000


class YOLO:
    def __init__(self, model_name: str, device: Optional[str] = None):
        # Vérification de la disponibilité de CUDA si nécessaire
        if device is not None and "cuda" in device and not torch.cuda.is_available():
            raise Exception("Vous avez demandé un device CUDA, mais il n'est pas disponible")
        elif device is None:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # Chargement du modèle
        self.model = torch.hub.load("ultralytics/yolov5", model_name, device=device)

    def __call__(self, img: Union[str, np.ndarray], conf_threshold: float = 0.25,
                 iou_threshold: float = 0.45, image_size: int = 720, agnostic: bool = False, multi_label: bool = True,
                 max_det: int = 50, amp: bool = True, classes: Optional[List[int]] = None) -> torch.tensor:
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


def yolo_detections_to_norfair_detections(yolo_detections: torch.tensor) -> List[Detection]:
    """convert detections_as_xywh to norfair detections"""
    norfair_detections: List[Detection] = []

    detections_as_xyxy = yolo_detections.xyxy[0]
    for detection_as_xyxy in detections_as_xyxy:
        bbox = np.array(
            [
                [detection_as_xyxy[0].item(), detection_as_xyxy[1].item()],
                [detection_as_xyxy[2].item(), detection_as_xyxy[3].item()],
            ]
        )
        scores = np.array(
            [detection_as_xyxy[4].item(), detection_as_xyxy[4].item()]
        )
        norfair_detections.append(
            Detection(
                points=bbox, scores=scores, label=int(detection_as_xyxy[-1].item())
            )
        )

    return norfair_detections


def detect(
        video_capture: cv2.VideoCapture,
        object_types: list[int],
        interval: float,
        display_detection: bool,
        display_fps: bool,
        yolov5_paramms: dict,
        bdd_params: dict
) -> None:
    log.info("Début de la détection")
    model = YOLO(yolov5_paramms["weights"], yolov5_paramms["device"])

    # for fps
    prev_frame_time = 0
    new_frame_time = 0

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
                classes=object_types,
                agnostic=yolov5_paramms["agnostic_nms"],
                multi_label=yolov5_paramms["multi_label_nms"],
                max_det=yolov5_paramms["max_det"],
                amp=yolov5_paramms["amp"],
            )
        except Exception as e:
            log.error("Erreur lors du traitement de l'image avec le modèle YOLOv5: {}".format(e))
            continue

        detections = yolo_detections_to_norfair_detections(results)

        try:
            # Utilisation de la librairie Sort pour suivre les personnes détectées
            tracked_objects = tracker.update(detections=detections)
        except Exception as e:
            log.error("Erreur lors du suivie des objets: {}".format(e))
            continue

        labels = [f"{a.id}" for a in tracked_objects]

        # Pause entre chaque détection si spécifiée
        if interval > 0:
            log.debug("Pause de " + str(interval) + " secondes")
            time.sleep(interval)

        # Affichage des images si spécifié
        if display_detection:
            # time when we finish processing for this frame
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = str(int(fps)) + " FPS"

            detections = sv.Detections.from_yolov5(results)
            frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

            # Affichage des FPS si spécifié
            if display_fps:
                cv2.putText(frame, fps, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()


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
    classes = base_params["classes"]
    interval = base_params["interval"]
    display_detection = base_params["display_detection"]
    display_fps = base_params["display_fps"]

    # Vérification de l'ouverture de la caméra
    if not video_capture.isOpened():
        log.error("Impossible d'ouvrir la source, verifier le fichier de configuration")
        return

    if display_detection:
        log.info("Pour quitter l'application, appuyez sur la touche 'q'")
    # Détection des personnes
    try:
        detect(video_capture, classes, interval, display_detection, display_fps, yolov5_paramms, bdd_params)
    except Exception as e:
        log.error("Erreur lors de la détection: {}".format(e))
