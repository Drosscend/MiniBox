import logging
log = logging.getLogger("main")

CALCUL_DIRECTION_NB_POSITIONS = 10

def calculate_direction(positions):
    if len(positions) < CALCUL_DIRECTION_NB_POSITIONS:
        return None

    dx_total = 0
    dy_total = 0
    for i in range(1, CALCUL_DIRECTION_NB_POSITIONS):
        x1, y1, _, _ = positions[-i-1]
        x2, y2, _, _ = positions[-i]
        dx = x2 - x1
        dy = y2 - y1
        dx_total += dx
        dy_total += dy

    dx_mean = dx_total / CALCUL_DIRECTION_NB_POSITIONS
    dy_mean = dy_total / CALCUL_DIRECTION_NB_POSITIONS

    if dx_mean > 0 and dy_mean > 0:
        return "bottom-right"
    elif dx_mean > 0 and dy_mean < 0:
        return "top-right"
    elif dx_mean < 0 and dy_mean > 0:
        return "bottom-left"
    elif dx_mean < 0 and dy_mean < 0:
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
        self.get_direction()
        if len(self.positions) > CALCUL_DIRECTION_NB_POSITIONS:
            self.positions.pop(0)

    def get_direction(self):
        direction = calculate_direction(self.positions)
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
