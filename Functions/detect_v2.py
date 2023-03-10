import cv2
import supervision as sv
from ultralytics import YOLO
import TrackedObjects
import sort

# Initialisation de la collection d'objets suivis
tracked_objects = TrackedObjects.TrackedObjects()

# Initialisation de la librairie Sort pour suivre les personnes détectées
model_sort = sort.Sort()

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

        # Pour vérifier que le modèle YOLOv8 est chargé et fonctionne correctement
        try:
            result = model(frame, agnostic_nms=False, verbose=False, conf=0.5, classes=[0])[0]
        except Exception as e:
            print("Erreur lors du traitement de l'image avec le modèle YOLOv8: {}".format(e))
            continue

        # Pour vérifier que la librairie Sort est chargée et fonctionne correctement
        try:
            track = model_sort.update(result.pred[0])
        except Exception as e:
            print("Erreur lors du suivie des objets: {}".format(e))
            continue

        detections = sv.Detections.from_yolov8(result)

        labels = [
            f"{tracked_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, tracked_id
            in detections
        ]
        
        for j in range(len(track.tolist())):
            # Récupère les informations sur l'objet
            tracked_object = track.tolist()[j]
            object_id = int(tracked_object[4])
            print(object_id)

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

        cv2.imshow('frame', frame)

        if cv2.waitKey(30) == 27:  # 27 = ESC
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Detection terminée")


if __name__ == '__main__':
    main()
