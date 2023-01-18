import cv2

from Functions import TrackedObjects


def draw_bounding_boxes(image, current: list[int], tracked_objects: TrackedObjects.TrackedObjects) -> None:
    """
    Dessine les boites englobantes des objets détectés
    @param image: Image sur laquelle dessiner les boites englobantes
    @param current: Liste des ids des objets détectés à l'instant t
    @param tracked_objects: Liste des objets détectés
    """
    # Si aucun objet n'a été détecté
    if not current:
        cv2.putText(image, "Aucun objet detecte", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for object_id in current:
            object_info = tracked_objects.get(object_id)
            if object_info is not None:
                confidence = format(object_info.confidence, ".2f")
                x1 = object_info.x1
                y1 = object_info.y1
                x2 = object_info.x2
                y2 = object_info.y2
                color = object_info.color
                direction = object_info.direction
                classe = object_info.classe

                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                text = f"id:{object_id}"
                text += f" - {classe}"
                text += f" - {confidence}"
                if direction:
                    text += f" - direction:({direction})"

                text_color = (255, 255, 255)
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(text, font, 0.7, 2)[0]
                text_x = x1 + 4
                text_w = text_size[0] + 10
                cv2.rectangle(image, (text_x - 5, y1 - 25), (text_x + text_w, y1), color, -1)
                cv2.putText(image, text, (text_x, y1 - 5), font, 0.7, text_color, 2)

    cv2.imshow("Video", image)
