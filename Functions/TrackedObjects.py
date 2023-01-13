"""
Ce code implémente une classe `TrackedObject` représentant un objet suivi dans une vidéo,
ainsi qu'une classe `TrackedObjects` gérant un ensemble d'objets suivis.

Chaque objet suivi est caractérisé par un identifiant unique, des coordonnées (x1, y1) et (x2, y2)
définissant un rectangle englobant l'objet, ainsi qu'une couleur.
Des méthodes sont fournies pour mettre à jour la position de l'objet et obtenir sa direction.

La direction de l'objet est calculée en utilisant les `CALCUL_DIRECTION_NB_POSITIONS` dernières positions
enregistrées. La vitesse de l'objet est également prise en compte, en comparant la distance parcourue à un seuil de
vitesse minimal ('SPEED_THRESHOLD`). Si la vitesse est supérieure au seuil, la direction de l'objet est déterminée en
fonction de la moyenne des déplacements sur l'axe des x et des y. Si la vitesse est inférieure au seuil, `None` est
retourné."""

import logging
import math

log = logging.getLogger("main")

CALCUL_DIRECTION_NB_POSITIONS = 4  # Nombre de positions à prendre en compte pour calculer la direction
SPEED_THRESHOLD = 10  # Vitesse minimale pour que la direction soit prise en compte


def calculate_direction(positions: list):
    """Calcul la direction de l'objet en fonction des positions enregistrées.

    Args:
        positions (list(int,int,int,int)): tableau de positions (x1, y1, x2, y2)

    Returns:
        string: direction de l'objet
    """
    total_distance = 0
    total_dx = 0
    total_dy = 0
    for i in range(1, CALCUL_DIRECTION_NB_POSITIONS):
        x1, y1, _, _ = positions[-i - 1]
        x2, y2, _, _ = positions[-i]
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)
        total_distance += distance
        total_dx += dx
        total_dy += dy

    mean_dx = total_dx / CALCUL_DIRECTION_NB_POSITIONS
    mean_dy = total_dy / CALCUL_DIRECTION_NB_POSITIONS
    mean_distance = total_distance / CALCUL_DIRECTION_NB_POSITIONS

    if mean_dx > 0 and mean_dy > 0:
        if mean_distance > SPEED_THRESHOLD:
            return "bottom-right"
    elif mean_dx > 0 > mean_dy:
        if mean_distance > SPEED_THRESHOLD:
            return "top-right"
    elif mean_dx < 0 < mean_dy:
        if mean_distance > SPEED_THRESHOLD:
            return "bottom-left"
    elif mean_dx < 0 and mean_dy < 0:
        if mean_distance > SPEED_THRESHOLD:
            return "top-left"
    else:
        return None


class TrackedObject:
    """Classe représentant un objet suivi dans une vidéo.
    """
    def __init__(self, obj_id:int, confidence:float, x1:int, y1:int, x2:int, y2:int, color:tuple):
        self.obj_id = obj_id
        self.confidence = confidence
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.positions = [(x1, y1, x2, y2)]
        self.direction = None

    def update_position(self, confidence:float, x1:int, y1:int, x2:int, y2:int):
        """Mise à jour de la position de l'objet.

        Args:
            confidence (float): confiance de l'objet
            x1 (int): coordonnée x du point en haut à gauche du rectangle englobant l'objet
            y1 (int): coordonnée y du point en haut à gauche du rectangle englobant l'objet
            x2 (int): coordonnée x du point en bas à droite du rectangle englobant l'objet
            y2 (int): coordonnée y du point en bas à droite du rectangle englobant l'objet
        """
        self.confidence = confidence
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.positions.append((x1, y1, x2, y2))
        if len(self.positions) > CALCUL_DIRECTION_NB_POSITIONS:
            self.positions.pop(0)
            self.set_direction()

    def set_direction(self):
        """Calcule la direction de l'objet en fonction des positions enregistrées.
        """
        direction = calculate_direction(self.positions)
        self.direction = direction

    def __str__(self):
        """Affichage de l'objet.

        Returns:
            string: description de l'objet
        """
        direction = self.direction
        text = f"\n id: {self.obj_id},\n Confidence: {self.confidence},\n positions: {self.x1}, {self.y1}, " \
               f"{self.x2}, {self.y2},\n couleur: {self.color}"
        if direction:
            text += f",\n direction: {direction}"
        return text


class TrackedObjects:
    """Classe représentant un ensemble d'objets suivi dans une vidéo.
    """
    def __init__(self):
        self.tracked_objects = []

    def add(self, obj_id:int, confidence:float, x1:int, y1:int, x2:int, y2:int, color:tuple):
        """Ajoute un objet à la liste des objets suivis.

        Args:
            obj_id (int): identifiant de l'objet
            confidence (float): confiance de l'objet
            x1 (int): coordonnée x du point en haut à gauche du rectangle englobant l'objet
            y1 (int): coordonnée y du point en haut à gauche du rectangle englobant l'objet
            x2 (int): coordonnée x du point en bas à droite du rectangle englobant l'objet
            y2 (int): coordonnée y du point en bas à droite du rectangle englobant l'objet
            color (tuple(int,int,int)): couleur de l'objet
        """
        tracked_object = TrackedObject(obj_id, confidence, x1, y1, x2, y2, color)
        self.tracked_objects.append(tracked_object)

    def get(self, obj_id:int):
        """Retourne l'objet correspondant à l'identifiant.

        Args:
            obj_id (int): identifiant de l'objet

        Returns:
            TrackedObject: objet correspondant à l'identifiant
        """
        for tracked_object in self.tracked_objects:
            if tracked_object.obj_id == obj_id:
                return tracked_object
        return None

    def remove(self, obj_id:int):
        """Supprime l'objet correspondant à l'identifiant.

        Args:
            obj_id (int): identifiant de l'objet
        """
        for i, tracked_object in enumerate(self.tracked_objects):
            if tracked_object.obj_id == obj_id:
                del self.tracked_objects[i]
                break

    def purge(self):
        self.tracked_objects = []
