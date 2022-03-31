import cv2

"""
Title: detector.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


async def detect(frame, aruco_dictionary):
    """
    Detects the aruco markers in the frame.

    Args:
        frame: The frame to detect markers in.
        aruco_dictionary: The aruco dictionary to use.

    Returns:
        A list of the detected markers.
    """
    aruco_parameters = cv2.aruco.DetectorParameters_create()
    return cv2.aruco.detectMarkers(frame, aruco_dictionary, parameters=aruco_parameters)
