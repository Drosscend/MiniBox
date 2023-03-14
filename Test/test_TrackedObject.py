import unittest

from Functions import TrackedObjects

TrackedObject = TrackedObjects.TrackedObject


class TestTrackedObject(unittest.TestCase):
    def test_init(self):
        # Test de création d'un objet suivi
        obj = TrackedObject(1, 50, 50, 100, 100, 0, (0, 0, 0))
        self.assertEqual(obj.obj_id, 1)
        self.assertEqual(obj.x1, 50)
        self.assertEqual(obj.y1, 50)
        self.assertEqual(obj.x2, 100)
        self.assertEqual(obj.y2, 100)
        self.assertEqual(obj.classe, 0)
        self.assertEqual(obj.color, (0, 0, 0))
        self.assertEqual(obj.positions, [(50, 50, 100, 100)])
        self.assertIsNone(obj.direction)

    def test_update_position(self):
        # Test de mise à jour de la position d'un objet suivi
        obj = TrackedObject(1, 50, 50, 100, 100, 0, (0, 0, 0))
        obj.update_position(55, 55, 105, 105)
        self.assertEqual(obj.positions, [(50, 50, 100, 100), (55, 55, 105, 105)])
        self.assertIsNone(obj.direction)

    def test_calculate_direction(self):
        # Test lorsque la personne ne bouge pas
        positions = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]
        direction = TrackedObjects.calculate_direction(positions)
        self.assertIsNone(direction)

        # Test lorsque la personne bouge vers en bas à gauche
        positions = [(221, 273, 481, 480), (219, 272, 481, 480), (218, 272, 481, 480), (168, 274, 481, 480)]
        direction = TrackedObjects.calculate_direction(positions)
        self.assertEqual(direction, "bottom-left")

        # Test lorsque la personne bouge vers en bas à droite
        positions = [(221, 273, 481, 480), (219, 272, 481, 480), (218, 272, 481, 480), (268, 274, 481, 480)]
        direction = TrackedObjects.calculate_direction(positions)
        self.assertEqual(direction, "bottom-right")

        # Test lorsque la personne bouge vers le haut à gauche
        positions = [(221, 273, 481, 480), (219, 272, 481, 480), (218, 272, 481, 480), (168, 174, 481, 480)]
        direction = TrackedObjects.calculate_direction(positions)
        self.assertEqual(direction, "top-left")

        # Test lorsque la personne bouge vers le haut à droite
        positions = [(221, 273, 481, 480), (219, 272, 481, 480), (218, 272, 481, 480), (268, 174, 481, 480)]
        direction = TrackedObjects.calculate_direction(positions)
        self.assertEqual(direction, "top-right")


if __name__ == "__main__":
    unittest.main()
