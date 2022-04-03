import cv2
import math
from .camera import CAMERA_RESOLUTIONS

"""
Project: QuickAR
Title: utils.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description:
"""


def convert_to_gray(frame):
    """
    This function is used to convert the frame to gray.

    args:
        frame: The frame to convert to gray.

    returns:
        The frame in grayscale.
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def convert_resolution(frame, resolution=CAMERA_RESOLUTIONS["default"]):
    """
    This function is used to convert a resolution to a tuple.

    args:
        frame: The frame to convert.c
        resolution: The resolution to convert.

    returns:
        The frame in the specified resolution.
    """
    return cv2.resize(frame, resolution)


class Pose:

    def __init__(self, x=0, y=0, z=0, yaw=0, pitch=0, roll=0, parent=None, child=None):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.parent = parent
        self.child = child

    @property
    def position(self):
        return self.x, self.y, self.z

    @property
    def rotation(self):
        return self.yaw, self.pitch, self.roll

    def is_comparable(self, other):
        pass

    def to_matrix(self):
        pass
