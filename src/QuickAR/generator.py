import cv2
import numpy as np

"""
Title: generator.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


async def generate_marker(aruco_dictionary, aruco_marker_id):
    # Create the ArUco marker
    marker = np.zeros((300, 300, 1), dtype="uint8")
    cv2.aruco.drawMarker(aruco_dictionary, aruco_marker_id, 300, marker, 1)
    return marker


async def generate_grid_board(aruco_dictionary, x=5, y=7, length=1, separation=0.8, image_size=(600, 500)):
    board = cv2.aruco.GridBoard_create(
        markersX=x,
        markersY=y,
        markerLength=length,
        markerSeparation=separation,
        dictionary=aruco_dictionary)
    img = board.draw(image_size)
    return board, img


async def generate_charuco_board(aruco_dictionary, x=5, y=7, square_length=0.04, marker_length=0.01,
                                 image_size=(600, 500)):
    charuco_board = cv2.aruco.CharucoBoard_create(
        squaresX=x,
        squaresY=y,
        squareLength=square_length,
        markerLength=marker_length,
        dictionary=aruco_dictionary)
    img = charuco_board.draw(image_size)
    return charuco_board, img
