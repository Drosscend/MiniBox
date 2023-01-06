import unittest
from Functions import TrackedObjects

TrackedObject = TrackedObjects.TrackedObject

class TestTrackedObject(unittest.TestCase):
    def test_init(self):
        # Test de création d'un objet suivi
        obj = TrackedObject(1, 0.99, 50, 50, 100, 100, "red")
        self.assertEqual(obj.obj_id, 1)
        self.assertEqual(obj.confidence, 0.99)
        self.assertEqual(obj.x1, 50)
        self.assertEqual(obj.y1, 50)
        self.assertEqual(obj.x2, 100)
        self.assertEqual(obj.y2, 100)
        self.assertEqual(obj.color, "red")
        self.assertEqual(obj.positions, [(50, 50, 100, 100)])
        self.assertIsNone(obj.direction)

    def test_update_position(self):
        # Test de mise à jour de la position d'un objet suivi
        obj = TrackedObject(1, 0.99, 50, 50, 100, 100, "red")
        obj.update_position(0.99, 55, 55, 105, 105)
        self.assertEqual(obj.positions, [(50, 50, 100, 100), (55, 55, 105, 105)])
        self.assertIsNone(obj.direction)

    def test_calculate_direction(self):
        # Test direction bottom-right with high speed
        positions = [(0, 0, 0, 0), (1, 1, 1, 1), (2, 2, 2, 2), (3, 3, 3, 3), (4, 4, 4, 4),
                    (5, 5, 5, 5), (6, 6, 6, 6), (7, 7, 7, 7), (8, 8, 8, 8), (9, 9, 9, 9)]
        direction = TrackedObjects.calculate_direction(positions, 0.1)
        self.assertEqual(direction, "bottom-right")

        # Test direction bottom-left with low speed
        positions = [(0, 0, 0, 0), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1),
                    (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1)]
        direction = TrackedObjects.calculate_direction(positions, 0.1)
        self.assertIsNone(direction)

        # Test direction top-left with high speed
        positions = [(9, 9, 9, 9), (8, 8, 8, 8), (7, 7, 7, 7), (6, 6, 6, 6), (5, 5, 5, 5),
                    (4, 4, 4, 4), (3, 3, 3, 3), (2, 2, 2, 2), (1, 1, 1, 1), (0, 0, 0, 0)]
        direction = TrackedObjects.calculate_direction(positions, 0.1)
        self.assertEqual(direction, "top-left")

        # Test direction top-right with low speed
        positions = [(1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1),
                    (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1)]
        direction = TrackedObjects.calculate_direction(positions, 0.1)
        self.assertIsNone(direction)

if __name__ == "__main__":
    unittest.main()