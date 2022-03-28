import cv2
import numpy as np
from .aruco_dict import ARUCO_DICT

"""
Title: generator.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


class MarkerGenerator:
    """
    MarkerGenerator class

    ----------

    Attributes

    -------

    Methods

    """

    def __init__(self, desired_aruco_dictionary):
        if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
            print("ArUCo tag type is not supported")
            exit(0)

        self.aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])

    def generate_marker(self, aruco_marker_id):
        # Create the ArUco marker
        marker = np.zeros((300, 300, 1), dtype="uint8")
        cv2.aruco.drawMarker(self.aruco_dictionary, aruco_marker_id, 300, marker, 1)
        return marker

    def generate_grid_board(self, x=5, y=7, length=0.04, separation=0.01):
        board = cv2.aruco.GridBoard_create(
            markersX=x,
            markersY=y,
            markerLength=length,
            markerSeparation=separation,
            dictionary=self.aruco_dictionary)
        img = board.draw((600, 500))
        return board, img

    def generate_charuco_board(self, x=5, y=7, square_length=0.04, marker_length=0.01):
        charuco_board = cv2.aruco.CharucoBoard_create(
            squaresX=x,
            squaresY=y,
            squareLength=square_length,
            markerLength=marker_length,
            dictionary=self.aruco_dictionary)
        img = charuco_board.draw((600, 500))
        return charuco_board, img
