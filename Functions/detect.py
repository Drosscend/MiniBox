import time
import torch
import logging
import cv2
import numpy as np

log = logging.getLogger("main")


def detect(webcam, classes, show=False):
    """
    Fonction de détection
    :param webcam: webcam à utiliser
    :param classes: type de détection (0: personnes, 1: vélos)
    :param show: affichage de la détection (True/False) (optionnel)
    :return: None
    Enregistre les résultats dans un fichier csv avec comme entête:
    date,occurence,type,positions
    """
    log.debug("Début de la détection")
    cam = cv2.VideoCapture(webcam)
    if show:
        log.warning("Affichage des résultats activé, pour fermer la fenêtre, appuyez sur la touche 'q'")

    while cam.isOpened():
        ret, frame = cam.read()
        # création du model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

        # paramètres du model
        model.classes = classes
        model.conf = 0.50  # NMS confidence threshold
        model.iou = 0.45  # NMS IoU threshold
        model.agnostic = False  # NMS class-agnostic
        model.multi_label = False  # NMS multiple labels per box
        model.max_det = 1000  # maximum number of detections per image
        model.amp = False  # Automatic Mixed Precision (AMP) inference

        # detection
        results = model(frame)  # 'OUTPUT/photo.jpg'

        generate_csv(results, classes)

        # affichage des images
        if show:
            cv2.imshow('YOLO', np.squeeze(results.render()))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cam.release()
    cv2.destroyAllWindows()
    log.debug("Detection terminée")


def generate_csv(results, classes):
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
        f.write(date + ',' + str(nb_personnes) + ',' + str(classes) + ',' + str(tab_of_positions) + '\r')
    log.debug("Résultats traités")
