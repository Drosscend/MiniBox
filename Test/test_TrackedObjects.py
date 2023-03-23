import unittest

from Functions import TrackedObjects

TrackedObjects = TrackedObjects.TrackedObjects


class TestTrackedObjects(unittest.TestCase):
    def test_add_and_get(self):
        # Create a TrackedObjects instance
        objs = TrackedObjects()

        # Add a tracked object with name_idx 0
        objs.add(0, 0, 0, 0, 0, 0)
        self.assertEqual(len(objs.tracked_objects), 1)

        # Get the tracked object with name_idx 0
        obj = objs.get(0)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.obj_id, 0)
        self.assertEqual(obj.x1, 0)
        self.assertEqual(obj.y1, 0)
        self.assertEqual(obj.x2, 0)
        self.assertEqual(obj.y2, 0)
        self.assertEqual(obj.classe, 0)

        # Try to get a tracked object with an invalid name_idx
        obj = objs.get(1)
        self.assertIsNone(obj)

    def test_remove(self):
        # Create a TrackedObjects instance
        objs = TrackedObjects()

        # Add two tracked objects with name_idx 0 and 1
        objs.add(0, 0, 0, 0, 0, 0)
        objs.add(1, 0, 0, 0, 0, 0)
        self.assertEqual(len(objs.tracked_objects), 2)

        # Remove the tracked object with name_idx 0
        objs.remove(0)
        self.assertEqual(len(objs.tracked_objects), 1)
        obj = objs.get(0)
        self.assertIsNone(obj)
        obj = objs.get(1)
        self.assertIsNotNone(obj)

        # Try to remove a tracked object with an invalid name_idx
        objs.remove(2)
        self.assertEqual(len(objs.tracked_objects), 1)

    def test_purge(self):
        # Create a TrackedObjects instance
        objs = TrackedObjects()

        # Add two tracked objects
        objs.add(0, 0, 0, 0, 0, 0)
        objs.add(1, 0, 0, 0, 0, 0)
        self.assertEqual(len(objs.tracked_objects), 2)

        # Purge tracked objects
        objs.purge()
        self.assertEqual(len(objs.tracked_objects), 0)


if __name__ == "__main__":
    unittest.main()
