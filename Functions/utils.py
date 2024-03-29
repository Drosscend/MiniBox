from typing import List

import numpy as np
import torch
from norfair import Detection


def yolo_detections_to_norfair_detections(yolo_detections: torch.tensor) -> List[Detection]:
    """
    Convertit les résultats de la détection YOLOv5 en format Norfair
    @param yolo_detections: Résultats de la détection YOLOv5
    @return: Résultats de la détection Norfair
    """
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


def get_label_by_name(label_id: int) -> str:
    """
    Retourne le nom de la classe à partir de son ID
    @param label_id: ID de la classe
    @return: Nom de la classe
    """
    names = {
        0: "person",
        1: "bicycle",
        2: "car",
        3: "motorcycle",
        4: "airplane",
        5: "bus",
        6: "train",
        7: "truck",
        8: "boat",
        9: "traffic light",
        10: "fire hydrant",
        11: "stop sign",
        12: "parking meter",
        13: "bench",
        14: "bird",
        15: "cat",
        16: "dog",
        17: "horse",
        18: "sheep",
        19: "cow",
        20: "elephant",
        21: "bear",
        22: "zebra",
        23: "giraffe",
        24: "backpack",
        25: "umbrella",
        26: "handbag",
        27: "tie",
        28: "suitcase",
        29: "frisbee",
        30: "skis",
        31: "snowboard",
        32: "sports ball",
        33: "kite",
        34: "baseball bat",
        35: "baseball glove",
        36: "skateboard",
        37: "surfboard",
        38: "tennis racket",
        39: "bottle",
        40: "wine glass",
        41: "cup",
        42: "fork",
        43: "knife",
        44: "spoon",
        45: "bowl",
        46: "banana",
        47: "apple",
        48: "sandwich",
        49: "orange",
        50: "broccoli",
        51: "carrot",
        52: "hot dog",
        53: "pizza",
        54: "donut",
        55: "cake",
        56: "chair",
        57: "couch",
        58: "potted plant",
        59: "bed",
        60: "dining table",
        61: "toilet",
        62: "tv",
        63: "laptop",
        64: "mouse",
        65: "remote",
        66: "keyboard",
        67: "cell phone",
        68: "microwave",
        69: "oven",
        70: "toaster",
        71: "sink",
        72: "refrigerator",
        73: "book",
        74: "clock",
        75: "vase",
        76: "scissors",
        77: "teddy bear",
        78: "hair drier",
        79: "toothbrush",
    }
    # retourne le nom de la classe avec la première lettre en majuscule
    return names[label_id].capitalize()


def initListOfDirections(classes: list) -> dict:
    """
    Initialise la liste des directions pour chaque classe
    @param classes: Liste des classes
    @return: Liste des directions
    """
    if not classes:
        raise ValueError("La liste des classes est vide")

    info_for_class = {
        "total": 0,
        "top-left": 0,
        "top-right": 0,
        "bottom-left": 0,
        "bottom-right": 0
    }
    list_of_directions = {}
    for classe in classes:
        list_of_directions[classe] = info_for_class.copy()

    return list_of_directions