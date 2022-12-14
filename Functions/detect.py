import time
import torch
import logging
import cv2
import numpy as np

log = logging.getLogger("main")

def detect(type, show=False):
    """
    Fonction de détection
    :param type: type de détection (0: personnes, 1: vélos)
    :return: None
    Enregistre les résultats dans un fichier csv avec comme entête:
    date,occurence,type,positions
    """
    log.debug("Début de la détection")
    cam = cv2.VideoCapture(0)
    if show:
        log.warning("Affichage des résultats activé, pour fermer la fenêtre, appuyez sur la touche 'q'")

    while cam.isOpened():
        ret, frame = cam.read()
        # création du model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

        # paramètres du model
        model.classes = type
        model.conf = 0.25  # NMS confidence threshold
        model.iou = 0.45  # NMS IoU threshold
        model.agnostic = False  # NMS class-agnostic
        model.multi_label = False  # NMS multiple labels per box
        model.max_det = 1000  # maximum number of detections per image
        model.amp = False  # Automatic Mixed Precision (AMP) inference  

        # detection
        results = model(frame) # 'OUTPUT/photo.jpg'

        # affichage des résultats
        if show:
            cv2.imshow('YOLO', np.squeeze(results.render()))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        log.debug("Traitement des résultats")
        # enregistrement et traitement des résultats
        data = results.pandas().xyxy[0]
        data = data.drop(columns=['name', 'confidence', 'class'])
        date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        tab_of_positions = data.values.tolist()
        nb_personnes = len(tab_of_positions)

        # enregistrement des données dans un fichier csv
        with open('OUTPUT/data.csv', 'a') as f:
            # si le fichier est vide, on écrit l'entête
            if f.tell() == 0:
                f.write("date,occurence,type,positions\n")
            f.write(date + ',' + str(nb_personnes) + ',' + str(type) + ',' + str(tab_of_positions) + '\r')
        log.debug("Résultats traités")

    cam.release()
    cv2.destroyAllWindows()
    log.debug("Detection terminée")
