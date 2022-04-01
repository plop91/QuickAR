import cv2

"""
Project: QuickAR
Title: detector.py
Author: Ian Sodersjerna
Created: 3/20/2022
Description: This file contains the Method for detecting the ArUco markers in an image.
"""


# TODO: Add a method to detect QR codes
# TODO: Add a method to detect boards

async def detect_marker(frame, aruco_dictionary, aruco_parameters=cv2.aruco.DetectorParameters_create()):
    """
    Detects the aruco markers in the frame.

    Args:
        frame: The frame to detect markers in.
        aruco_dictionary: The aruco dictionary to use.
        aruco_parameters: The aruco parameters to use.

    Returns:
        A list of the detected markers.
    """
    return cv2.aruco.detectMarkers(frame, aruco_dictionary, parameters=aruco_parameters)
