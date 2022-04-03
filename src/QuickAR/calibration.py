import os.path
import cv2
import numpy as np

"""
Project: QuickAR
Title: calibration.py
Author: Ian Sodersjerna
Created: 3/20/2022
Description: This file contains methods to calibrate a camera.
"""


async def calibrate_from_grid_board(image, corners, board):
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

    if ret:
        return camera_matrix, dist_coeffs
    else:
        return None, None


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
    if len(corners) != len(ids):
        raise ValueError("The number of corners and ids must be the same.")
    ret, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraAruco(
        corners=corners,
        ids=ids,
        counter=35,
        board=board,
        imageSize=image.shape[::-1],
        cameraMatrix=None,
        distCoeffs=None)
    if ret:
        return camera_matrix, dist_coeffs
    else:
        return None, None


async def calibrate_from_charuco_board(image, board):
    """
    Calibrates the camera using the charuco board.

    Args:
        image: The image to be used for calibration.
        board: The charuco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    ret, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraCharuco(
        charucoCorners=image,
        charucoIds=board.ids,
        board=board,
        imageSize=image[0].shape,
        cameraMatrix=None,
        distCoeffs=None)
    if ret:
        return camera_matrix, dist_coeffs
    else:
        return None, None


async def calibrate_from_images(images, corners, board):
    """
    Calibrates the camera using the aruco board.

    Args:
        images: The images to be used for calibration.
        corners: The corners of the aruco boards.
        board: The aruco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    if len(images) != len(corners):
        raise ValueError("The number of images and corners must be the same.")
    combined = zip(images, corners)
    camera_matrix_list = []
    dist_coeffs_list = []
    for image in combined:
        ret, camera_matrix, dist_coeffs = calibrate_from_grid_board(image, board)
        if ret:
            camera_matrix_list.append(camera_matrix)
            dist_coeffs_list.append(dist_coeffs)

    if len(camera_matrix_list) == 0:
        return False, None, None

    mean_camera_matrix = np.mean(camera_matrix_list, axis=0)
    mean_dist_coeffs = np.mean(dist_coeffs_list, axis=0)

    if ret:
        return mean_camera_matrix, mean_dist_coeffs
    else:
        return None, None


async def calibrate_from_aruco_images(images, board):
    """
    Calibrates the camera using the aruco board.

    Args:
        images: The images to be used for calibration.
        board: The aruco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    ret = False
    for image in images:
        ret, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraAruco(
            corners=image,
            ids=board.ids,
            counter=35,
            board=board,
            imageSize=image[0].shape,
            cameraMatrix=None,
            distCoeffs=None)
    if ret:
        return camera_matrix, dist_coeffs
    else:
        return None, None


async def calibrate_from_charuco_images(images, board):
    """
    Calibrates the camera using the charuco board.

    Args:
        images: The images to be used for calibration.
        board: The charuco board.

    Returns:
        ret: The return value of the calibration.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    ret = False
    for image in images:
        ret, camera_matrix, dist_coeffs, _, _ = cv2.aruco.calibrateCameraCharuco(
            charucoCorners=image,
            charucoIds=board.ids,
            board=board,
            imageSize=image[0].shape,
            cameraMatrix=None,
            distCoeffs=None)
    if ret:
        return camera_matrix, dist_coeffs
    else:
        return None, None


async def warp_image(image, camera_matrix, dist_coeffs):
    """
    Warps an image using the camera matrix and distortion coefficients.

    Args:
        image: The image to be warped.
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.

    Returns:
        image: The warped image.
    """
    return cv2.undistort(image, camera_matrix, dist_coeffs)


async def save_calibration(camera_matrix, dist_coeffs):
    """
    Saves the camera matrix and distortion coefficients to a file.

    Args:
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    if not os.path.isdir("configs"):
        os.mkdir("configs")

    with open('configs/camera_matrix.npy', 'wb') as f:
        np.save(f, camera_matrix)

    with open('configs/dist_coeffs.npy', 'wb') as f:
        np.save(f, dist_coeffs)


async def load_calibration():
    """
    Loads the camera matrix and distortion coefficients from a file.

    Returns:
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    with open('configs/camera_matrix.npy', 'rb') as f:
        camera_matrix = np.load(f)

    with open('configs/dist_coeffs.npy', 'rb') as f:
        dist_coeffs = np.load(f)
    return camera_matrix, dist_coeffs


async def create_zero_calibration():
    """
    Creates a zero calibration.

    Returns:
        camera_matrix: The camera matrix.
        dist_coeffs: The distortion coefficients.
    """
    camera_matrix = await create_zero_camera_matrix()
    dist_coeffs = await create_zero_dist_coeffs()
    return camera_matrix, dist_coeffs


async def create_zero_dist_coeffs():
    """
    Creates a zero distortion coefficients array.

    Returns:
        dist_coeffs: The distortion coefficients.
    """
    dist_coeffs = np.zeros((5, 1))
    return dist_coeffs


async def create_zero_camera_matrix():
    """
    Creates a zero camera matrix array.

    Returns:
        camera_matrix: The camera matrix.
    """
    camera_matrix = np.zeros((3, 3))
    return camera_matrix
