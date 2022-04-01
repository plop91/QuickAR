import cv2
import numpy as np
"""
Project: QuickAR
Title: generator.py
Author: Ian Sodersjerna
Created: 3/20/2022
Description: This file contains the methods for generating ArUco markers and boards.
"""


async def generate_marker(aruco_dictionary, aruco_marker_id):
    """
    Generates a marker image from a dictionary and a marker id.

    Args:
        aruco_dictionary: The dictionary to use for the marker.
        aruco_marker_id: The id of the marker.
    """
    # Create the ArUco marker
    marker = np.zeros((300, 300, 1), dtype="uint8")
    cv2.aruco.drawMarker(aruco_dictionary, aruco_marker_id, 300, marker, 1)
    return marker


async def generate_grid_board(aruco_dictionary,
                              x=5,
                              y=7,
                              length=1,
                              separation=0.8,
                              image_size=(600, 500)):
    """
    Generates a grid board.

    Args:
        aruco_dictionary: The dictionary to use for the board.
        x: The number of markers in the x direction.
        y: The number of markers in the y direction.
        length: The length of each square.
        separation: The separation between each square.
        image_size: The size of the image to generate.
    """
    board = cv2.aruco.GridBoard_create(
        markersX=x,
        markersY=y,
        markerLength=length,
        markerSeparation=separation,
        dictionary=aruco_dictionary)
    img = board.draw(image_size)
    return board, img


async def generate_charuco_board(aruco_dictionary,
                                 x=5,
                                 y=7,
                                 square_length=0.04,
                                 marker_length=0.01,
                                 image_size=(600, 500)):
    """
    Generates a charuco board.

    Args:
        aruco_dictionary: The dictionary to use for the board.
        x: The number of markers in the x direction.
        y: The number of markers in the y direction.
        square_length: The length of each square.
        marker_length: The length of each marker.
        image_size: The size of the image to generate.
    """
    charuco_board = cv2.aruco.CharucoBoard_create(
        squaresX=x,
        squaresY=y,
        squareLength=square_length,
        markerLength=marker_length,
        dictionary=aruco_dictionary)
    img = charuco_board.draw(image_size)
    return charuco_board, img
