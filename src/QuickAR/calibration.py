import cv2
import pickle

"""
Title: calibration.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


async def calibrate_from_board(image, corners, board):
    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(
        objectPoints=board.objPoints,
        imagePoints=corners,
        imageSize=image.shape,  # [::-1], # may instead want to use gray.size
        cameraMatrix=None,
        distCoeffs=None)
    return ret, camera_matrix, dist_coeffs


async def calibrate_from_aruco_board(image, corners, ids, board):
    ret, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraAruco(
        corners=corners,
        ids=ids,
        counter=35,
        board=board,
        imageSize=image.shape[::-1],
        cameraMatrix=None,
        distCoeffs=None)
    return ret, camera_matrix, dist_coeffs


async def save_calibration(camera_matrix, dist_coeffs):
    with open('camera_matrix.pkl', 'wb') as f:
        pickle.dump(camera_matrix, f)

    with open('dist_coeffs.pkl', 'wb') as f:
        pickle.dump(dist_coeffs, f)


async def load_calibration():
    with open('camera_matrix.pkl', 'rb') as f:
        camera_matrix = pickle.load(f)

    with open('dist_coeffs.pkl', 'rb') as f:
        dist_coeffs = pickle.load(f)
    return camera_matrix, dist_coeffs
