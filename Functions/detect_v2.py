import cv2
import supervision as sv
from ultralytics import YOLO

import TrackedObjects

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()


def main():
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("TLS_ParcDuCanal.mp4")
    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while cap.isOpened():
        success, frame = cap.read()

        # Si le frame n'a pas pu être récupéré ou si la vidéo est terminée, quitte la boucle
        if not success:
            break

        # Pour vérifier que le modèle YOLOv5 est chargé et fonctionne correctement
        try:
            result = model(frame, agnostic_nms=False, verbose=False, conf=0.5, classes=[0])[0]
        except Exception as e:
            print("Erreur lors du traitement de l'image avec le modèle YOLOv8: {}".format(e))
            continue

        detections = sv.Detections.from_yolov8(result)

        labels = [
            f"{tracked_id} {model.model.names[class_id]} {confidence:0.2f}"
            for xyxy, confidence, class_id, tracked_id
            in detections
        ]

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

        # Supprime les objets qui n'ont pas été détectés dans le frame courant
        for tracked_object in tracked_objects.tracked_objects:
            if tracked_object.obj_id not in current:
                tracked_objects.remove(tracked_object.obj_id)
                print("Suppression de l'objet: {}".format(tracked_object.obj_id))

        cv2.imshow('frame', frame)

        if cv2.waitKey(30) == 27:  # 27 = ESC
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Detection terminée")


if __name__ == '__main__':
    main()
