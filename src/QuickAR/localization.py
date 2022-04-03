import cv2

"""
Project: QuickAR
Title: localization.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description: contains functions for localization
"""


async def pose_marker(corners, marker_length, camera_matrix, dist_coeffs):
    """
    Calculates the pose of a marker given the corners of the marker in the image

    Args:
        corners: the corners of the marker in the image
        marker_length: the length of the marker
        camera_matrix: the camera matrix
        dist_coeffs: the distortion coefficients

    Returns:
        the pose of the marker
        rvec: the rotation vector
        tvec: the translation vector
    """
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)
    return rvecs, tvecs


async def pose_grid_board(corners, ids, board, camera_matrix, dist_coeffs):
    """
    Calculates the pose of a grid board given the corners of the board in the image

    Args:
        corners: the corners of the board in the image
        ids: the ids of the markers in the board
        board: the board
        camera_matrix: the camera matrix
        dist_coeffs: the distortion coefficients

    Returns:
        the pose of the board
        rvec: the rotation vector
        tvec: the translation vector
    """
    rvecs, tvecs, _ = cv2.aruco.estimatePoseBoard(corners, ids, board, camera_matrix, dist_coeffs)
    return rvecs, tvecs


async def pose_charuco_board(corners, ids, board, camera_matrix, dist_coeffs):
    """
    Calculates the pose of a charuco board given the corners of the board in the image

    Args:
        corners: the corners of the board in the image
        ids: the ids of the markers in the board
        board: the board
        camera_matrix: the camera matrix
        dist_coeffs: the distortion coefficients

    Returns:
        the pose of the board
        rvec: the rotation vector
        tvec: the translation vector
    """
    rvecs, tvecs, _ = cv2.aruco.estimatePoseCharucoBoard(corners, ids, board, camera_matrix, dist_coeffs)
    return rvecs, tvecs
