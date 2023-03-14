from typing import List, Optional, Union
import numpy as np
import torch
import cv2
from norfair import Detection, Tracker, draw_boxes

DISTANCE_THRESHOLD_BBOX: float = 0.7
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
                 iou_threshold: float = 0.45, image_size: int = 720, classes: Optional[List[int]] = None) -> torch.tensor:
        self.model.conf = conf_threshold
        self.model.iou = iou_threshold
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


img_size=640
conf_threshold=0.25
iou_threshold=0.45
model_name = "yolov5n"
device = "cpu" # sinon 0
distance_function = "iou"
classes = [0,1]

model = YOLO(model_name, device=device)

cap = cv2.VideoCapture("2.mp4")
# cap = cv2.VideoCapture(0)

distance_threshold = DISTANCE_THRESHOLD_BBOX
tracker = Tracker(
    distance_function=distance_function,
    distance_threshold=distance_threshold,
)
    
while(True):
    ret, frame = cap.read()

    yolo_detections = model(
        frame,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold,
        image_size=img_size,
        classes=classes
    )
    detections = yolo_detections_to_norfair_detections(yolo_detections)
    tracked_objects = tracker.update(detections=detections)
    
    for a in tracked_objects:
        print("id", a.id, "points", a.last_detection.points)

    draw_boxes(frame, tracked_objects, draw_ids=True)

    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()