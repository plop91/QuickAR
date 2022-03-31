import cv2

"""
Title: detector.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


async def detect(frame, aruco_dictionary):
    aruco_parameters = cv2.aruco.DetectorParameters_create()
    return cv2.aruco.detectMarkers(frame, aruco_dictionary, parameters=aruco_parameters)
