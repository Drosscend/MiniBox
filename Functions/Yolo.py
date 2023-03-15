import logging
from typing import List, Optional, Union
import numpy as np
import torch

log = logging.getLogger("main")


class YOLO:
    def __init__(self, model_name: str, device: str, verbose: bool):
        """
        @param model_name: Nom du modèle à charger
        @param device: Device sur lequel le modèle doit être chargé
        @param verbose: Afficher les informations de chargement du modèle
        """
        # Vérification de la disponibilité de CUDA si nécessaire
        if device != "cpu"and not torch.cuda.is_available():
            log.error("Vous avez demandé un device CUDA, mais il n'est pas disponible")
            exit(1)

        # Chargement du modèle
        self.model = torch.hub.load("ultralytics/yolov5", model_name, device=device, verbose=verbose)

    def __call__(self,
                 img: Union[str, np.ndarray],
                 conf_threshold: float = 0.25,
                 iou_threshold: float = 0.45,
                 agnostic: bool = False,
                 multi_label: bool = True,
                 max_det: int = 50,
                 amp: bool = True, 
                 classes: Optional[List[int]] = None
                ) -> torch.tensor:
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
        self.model.agnostic = agnostic 
        self.model.multi_label = multi_label
        self.model.max_det = max_det
        self.model.amp = amp

        # si aucune classe n'est spécifiée, on utilise toutes les classes
        if classes is not None:
            self.model.classes = classes
        detections = self.model(img, size=640)
        return detections