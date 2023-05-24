import unittest

from Functions.utils import get_label_by_name, initListOfDirections


class TestYOLOToNorfair(unittest.TestCase):

    def test_get_label_by_name(self):
        # Tester la correspondance de tous les noms de classes avec leurs ID
        for label_id, label_name in {
            0: "person",
            1: "bicycle",
            2: "car",
            # etc.
        }.items():
            self.assertEqual(get_label_by_name(label_id), label_name.capitalize())


class TestInitListOfDirections(unittest.TestCase):
    def test_initListOfDirections(self):
        classes = [0, 1]
        expected_output = {
            0: {
                "total": 0,
                "top-left": 0,
                "top-right": 0,
                "bottom-left": 0,
                "bottom-right": 0
            },
            1: {
                "total": 0,
                "top-left": 0,
                "top-right": 0,
                "bottom-left": 0,
                "bottom-right": 0
            }
        }
        self.assertEqual(initListOfDirections(classes), expected_output)

    def test_initListOfDirections_empty(self):
        classes = []
        with self.assertRaises(ValueError):
            initListOfDirections(classes)


if __name__ == "__main__":
    unittest.main()
