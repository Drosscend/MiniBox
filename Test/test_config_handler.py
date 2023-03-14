import configparser
import unittest

from Functions.config_handler import check_params, get_base_params, get_yolov5_params, get_bdd_params


class TestConfigHandler(unittest.TestCase):
    def setUp(self):
        self.valid_config = configparser.ConfigParser()
        self.valid_config.read("config.ini")
        self.invalid_config = configparser.ConfigParser()
        self.invalid_config.read("invalid_config.ini")

    def test_check_params(self):
        self.assertTrue(check_params(self.valid_config))
        self.assertFalse(check_params(self.invalid_config))

    def test_get_base_params(self):
        base_params = get_base_params(self.valid_config)
        self.assertEqual(base_params['source'], 0)
        self.assertEqual(base_params['classes'], [1])
        self.assertEqual(base_params['interval'], 1)
        self.assertFalse(base_params['display_detection'])
        self.assertTrue(base_params['display_fps'])
        self.assertFalse(base_params['debug'])
        self.assertTrue(base_params['save_in_csv'])

    def test_get_yolov5_params(self):
        yolov5_params = get_yolov5_params(self.valid_config)
        self.assertEqual(yolov5_params['weights'], "yolov5m")
        self.assertEqual(yolov5_params['conf_thres'], 0.45)
        self.assertEqual(yolov5_params['iou_thres'], 0.45)
        self.assertFalse(yolov5_params['agnostic_nms'])
        self.assertTrue(yolov5_params['multi_label_nms'])
        self.assertEqual(yolov5_params['max_det'], 50)
        self.assertTrue(yolov5_params['amp'])
        self.assertEqual(yolov5_params['output_folder'], "OUTPUT")
        self.assertEqual(yolov5_params['csv_name'], "data.csv")
        self.assertEqual(yolov5_params['device'], "cpu")

    def test_get_bdd_params(self):
        bdd_params = get_bdd_params(self.valid_config)
        self.assertTrue(bdd_params['save_in_bdd'])
        self.assertEqual(bdd_params['bdd_name'], "detect_save.db")
        self.assertEqual(bdd_params['table_name'], "detect")
        self.assertEqual(bdd_params['time_to_save'], "00:00:00")
        self.assertFalse(bdd_params['keep_csv'])


if __name__ == "__main__":
    unittest.main()
