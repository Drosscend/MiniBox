import logging
log = logging.getLogger("main")

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
        self.positions.append((x1, y1, x2, y2))  # Ajout de la nouvelle position à la liste
        self.get_direction()
        if len(self.positions) > 10:
            self.positions.pop(0)

    def get_direction(self):
        if len(self.positions) < 5:
            return None

        dx_total = 0
        dy_total = 0
        for i in range(1, 5):
            x1, y1, _, _ = self.positions[-i-1]
            x2, y2, _, _ = self.positions[-i]
            dx = x2 - x1
            dy = y2 - y1
            dx_total += dx
            dy_total += dy

        dx_mean = dx_total / 5
        dy_mean = dy_total / 5

        if dx_mean > 0 and dy_mean > 0:
            self.direction = "bottom-right"
        elif dx_mean > 0 and dy_mean < 0:
            self.direction = "top-right"
        elif dx_mean < 0 and dy_mean > 0:
            self.direction = "bottom-left"
        elif dx_mean < 0 and dy_mean < 0:
            self.direction = "top-left"
        else:
            self.direction = None

    def __str__(self):
        direction = self.direction
        text = f"\nid: {self.name_idx},\n positions: {self.x1}, {self.y1}, {self.x2}, {self.y2},\n couleur: {self.color}"
        if direction:
            text += f",\n direction: {direction}"
        return text


class TrackedObjects:
    def __init__(self):
        self.tracked_objects = {}

    def add(self, name_idx, x1, y1, x2, y2, color):
        self.tracked_objects[name_idx] = TrackedObject(name_idx, x1, y1, x2, y2, color)

    def get(self, name_idx):
        return self.tracked_objects[name_idx]
    
    def remove(self, name_idx):
        del self.tracked_objects[name_idx]

    def update(self, name_idx, x1, y1, x2, y2):
        self.tracked_objects[name_idx].update_position(x1, y1, x2, y2)

    def get_all(self):
        return self.tracked_objects

    def showDict(self):
        for key in self.tracked_objects:
            log.debug(self.tracked_objects[key])

    def purge(self):
        self.tracked_objects = {}
