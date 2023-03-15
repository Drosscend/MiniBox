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
