import unittest
from Functions.utils import get_label_by_name


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


if __name__ == "__main__":
    unittest.main()
