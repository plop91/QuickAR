#!/usr/bin/env python3
import numpy as np
import os
import cv2
import QuickAR
import asyncio
import argparse

"""
Project: QuickAR
Title: create_calibration_config_from_images.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: This script will create and save a calibration matrix configuration for a camera.
"""


async def main(args):
    aruco_dict = QuickAR.get_aruco_dict(args.aruco_dictionary)
    parameters = QuickAR.get_aruco_parameters()

    board, _ = await QuickAR.generate_grid_board(aruco_dict)
    charuco_board, _ = await QuickAR.generate_charuco_board(aruco_dict)

    files = os.listdir("images")
    image_files = [f for f in files if f.endswith(".png")]
    training_image_files = [f for f in image_files if f.startswith("training")]

    training_images = []
    for image_file in training_image_files:
        image = cv2.imread(os.path.join("images", image_file))
        training_images.append(image)

    camera_matrix_list = []
    dist_coeffs_list = []

    for frame in training_images:
        if frame is not None:
            # grayscale image
            gray = QuickAR.convert_to_gray(frame)
            # Detect Aruco markers
            corners, ids = await QuickAR.detect_marker(gray, aruco_dict, parameters)
            # Make sure markers were detected before continuing
            if ids is not None and \
                    corners is not None and \
                    0 < len(ids) == len(corners):

                if len(corners) == board.getGridSize()[0] * board.getGridSize()[1]:
                    camera_matrix, dist_coeffs = await QuickAR.calibrate_from_grid_board(gray, corners, board)

                    # Print matrix and distortion coefficient to the console
                    if camera_matrix is not None and dist_coeffs is not None:
                        print(f"camera matrix: {camera_matrix}  ::: dist coeffs: {dist_coeffs}")
                        camera_matrix_list.append(camera_matrix)
                        dist_coeffs_list.append(dist_coeffs)

        # Exit at the end of the video on the EOF key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    mean_camera_matrix = np.mean(camera_matrix_list, axis=0)
    mean_dist_coeffs = np.mean(dist_coeffs_list, axis=0)
    await QuickAR.save_calibration(mean_camera_matrix, mean_dist_coeffs)
    print(f"average camera matrix: {mean_camera_matrix}  ::: average dist coeffs: {mean_dist_coeffs}")


if __name__ == "__main__":
    print(__doc__)
    parser = argparse.ArgumentParser(description='Example of renderer functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    arguments = parser.parse_args()
    asyncio.run(main(arguments))
