import unittest
import QuickAR


class TestArucoDict(unittest.TestCase):

    def test_get_aruco_dict(self):
        self.assertIsNotNone(QuickAR.get_aruco_dict("DICT_ARUCO_ORIGINAL"))


if __name__ == '__main__':
    unittest.main()
