import time
import os
import torch
import logging

log = logging.getLogger("main")

def detect(source, type):
    """
    Fonction de détection
    :param source: source de la photo
    :param type: type de détection (0: personnes, 1: vélos)
    :return: None
    Enregistre les résultats dans un fichier csv avec comme entête:
    date,occurence,type,positions
    """
    log.debug("Début de la détection")
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
    results = model(source) # 'OUTPUT/photo.jpg'
    log.debug("Detection terminée")

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
