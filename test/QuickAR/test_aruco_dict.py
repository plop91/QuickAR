import unittest
import QuickAR
"""
Project: QuickAR
Title: test_aruco_dict.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: Test cases for the aruco_dict module.
"""


class TestArucoDict(unittest.TestCase):

    def test_get_aruco_dict(self):
        self.assertIsNotNone(QuickAR.get_aruco_dict("DICT_ARUCO_ORIGINAL"))


if __name__ == '__main__':
    unittest.main()
