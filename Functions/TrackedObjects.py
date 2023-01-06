"""
Ce code implémente une classe `TrackedObject` représentant un objet suivi dans une vidéo,
ainsi qu'une classe `TrackedObjects` gérant un ensemble d'objets suivis.

Chaque objet suivi est caractérisé par un identifiant unique, des coordonnées (x1, y1) et (x2, y2)
définissant un rectangle englobant l'objet, ainsi qu'une couleur.
Des méthodes sont fournies pour mettre à jour la position de l'objet et obtenir sa direction.

La direction de l'objet est calculée en utilisant les `CALCUL_DIRECTION_NB_POSITIONS` dernières positions enregistrées.
La vitesse de l'objet est également prise en compte, en comparant la distance parcourue à un seuil de vitesse minimal (`SPEED_THRESHOLD`).
Si la vitesse est supérieure au seuil, la direction de l'objet est déterminée en fonction de la moyenne des déplacements sur l'axe des x et des y.
Si la vitesse est inférieure au seuil, `None` est retourné.
"""

import logging
import math
log = logging.getLogger("main")

CALCUL_DIRECTION_NB_POSITIONS = 10 # Nombre de positions à prendre en compte pour calculer la direction
SPEED_THRESHOLD = 10 # Vitesse minimale pour que la direction soit prise en compte

def calculate_direction(positions, relative_value):
    if len(positions) < CALCUL_DIRECTION_NB_POSITIONS:
        return None

    total_distance = 0
    total_dx = 0
    total_dy = 0
    for i in range(1, CALCUL_DIRECTION_NB_POSITIONS):
        x1, y1, _, _ = positions[-i-1]
        x2, y2, _, _ = positions[-i]
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)
        total_distance += distance
        total_dx += dx
        total_dy += dy

    mean_dx = total_dx / CALCUL_DIRECTION_NB_POSITIONS
    mean_dy = total_dy / CALCUL_DIRECTION_NB_POSITIONS
    mean_distance = total_distance / CALCUL_DIRECTION_NB_POSITIONS
    mean_speed = mean_distance / relative_value

    if mean_dx > 0 and mean_dy > 0:
        if mean_speed > SPEED_THRESHOLD:
            return "bottom-right"
    elif mean_dx > 0 and mean_dy < 0:
        if mean_speed > SPEED_THRESHOLD:
            return "top-right"
    elif mean_dx < 0 and mean_dy > 0:
        if mean_speed > SPEED_THRESHOLD:
            return "bottom-left"
    elif mean_dx < 0 and mean_dy < 0:
        if mean_speed > SPEED_THRESHOLD:
            return "top-left"
    else:
        return None


class TrackedObject:
    def __init__(self, name_idx, x1, y1, x2, y2, color):
        self.name_idx = name_idx
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.positions = [(x1, y1, x2, y2)]
        self.direction = None

    def update_position(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.positions.append((x1, y1, x2, y2))
        self.set_direction()
        if len(self.positions) > CALCUL_DIRECTION_NB_POSITIONS:
            self.positions.pop(0)

    def set_direction(self):
        direction = calculate_direction(self.positions, 0.1)
        self.direction = direction

    def __str__(self):
        direction = self.direction
        text = f"\n id: {self.name_idx},\n positions: {self.x1}, {self.y1}, {self.x2}, {self.y2},\n couleur: {self.color}"
        if direction:
            text += f",\n direction: {direction}"
        return text


class TrackedObjects:
    def __init__(self):
        self.tracked_objects = []

    def add(self, name_idx, x1, y1, x2, y2, color):
        tracked_object = TrackedObject(name_idx, x1, y1, x2, y2, color)
        self.tracked_objects.append(tracked_object)

    def get(self, name_idx):
        for tracked_object in self.tracked_objects:
            if tracked_object.name_idx == name_idx:
                return tracked_object
        return None

    def remove(self, name_idx):
        for i, tracked_object in enumerate(self.tracked_objects):
            if tracked_object.name_idx == name_idx:
                del self.tracked_objects[i]
                break

    def purge(self):
        self.tracked_objects = []
