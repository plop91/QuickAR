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
    """
    Calibrates the camera using the aruco board.

    Args:
        image: The image to be used for calibration.
        corners: The corners of the aruco board.
        board: The aruco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(
        objectPoints=board.objPoints,
        imagePoints=corners,
        imageSize=image.shape,  # [::-1], # may instead want to use gray.size
        cameraMatrix=None,
        distCoeffs=None)
    return ret, camera_matrix, dist_coeffs


async def calibrate_from_aruco_board(image, corners, ids, board):
    """
    Calibrates the camera using the aruco board.

    Args:
        image: The image to be used for calibration.
        corners: The corners of the aruco board.
        ids: The ids of the aruco board.
        board: The aruco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
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
    """
    Saves the camera matrix and distortion coefficients to a file.

    Args:
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    with open('camera_matrix.pkl', 'wb') as f:
        pickle.dump(camera_matrix, f)

    with open('dist_coeffs.pkl', 'wb') as f:
        pickle.dump(dist_coeffs, f)


async def load_calibration():
    """
    Loads the camera matrix and distortion coefficients from a file.

    Returns:
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    with open('camera_matrix.pkl', 'rb') as f:
        camera_matrix = pickle.load(f)

    with open('dist_coeffs.pkl', 'rb') as f:
        dist_coeffs = pickle.load(f)
    return camera_matrix, dist_coeffs
