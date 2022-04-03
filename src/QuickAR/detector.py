import cv2
from .aruco_dict import *

"""
Project: QuickAR
Title: detector.py
Author: Ian Sodersjerna
Created: 3/20/2022
Description: This file contains the Method for detecting the ArUco markers in an image.
"""


# TODO: Add a method to detect boards

async def detect_marker(frame,
                        aruco_dictionary=get_aruco_dict('default'),
                        aruco_parameters=get_aruco_parameters()):
    """
    Detects the aruco markers in the frame.

    Args:
        frame: The frame to detect markers in.
        aruco_dictionary: The aruco dictionary to use.
        aruco_parameters: The aruco parameters to use.

    Returns:
          The corners and ids of the detected markers.
    """
    corners, ids, _ = cv2.aruco.detectMarkers(frame,
                                              aruco_dictionary,
                                              parameters=aruco_parameters)
    if len(corners) == 0:
        return None, None
    return corners, ids


async def interpolate_grid_board(frame, corners, ids, board):
    """
    Interprets the detected markers.

    Args:
        frame: The frame to interpret the markers in.
        corners: The corners of the detected markers.
        ids: The ids of the detected markers.
        board: The board to

    Returns:
          The corners and ids of the detected markers.
    """
    response, charuco_corners, charuco_ids = cv2.aruco.interpolateCorners(
        markerCorners=corners,
        markerIds=ids,
        image=frame,
        board=board)
    return response, charuco_corners, charuco_ids


async def detect_marker_qr(frame):
    """
    Detects the QR codes in the frame.

    Args:
        frame: The frame to detect markers in.

    Returns:
          The corners and ids of the detected markers.
    """
    qr_code_detector = cv2.QRCodeDetector()
    decoded_text, points, _ = qr_code_detector.detectAndDecode(frame)
    return decoded_text, points
