import unittest
import QuickAR
"""
Project: QuickAR
Title: test_camera.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: Test cases for the camera class.
"""


class TestCamera(unittest.TestCase):

    def test_camera(self):
        camera = QuickAR.Camera()
        self.assertIsInstance(camera, QuickAR.Camera)


if __name__ == '__main__':
    unittest.main()
