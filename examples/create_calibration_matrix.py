#!/usr/bin/env python3
import numpy as np
import cv2
import QuickAR
import asyncio
"""
Project: QuickAR
Title: create_calibration_matrix.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: This script will create and save a calibration matrix for a camera.
"""


async def main():
    import argparse
    parser = argparse.ArgumentParser(description='Example of renderer functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    args = parser.parse_args()

    desired_aruco_dictionary = args.aruco_dictionary
    aruco_dict = cv2.aruco.Dictionary_get(desired_aruco_dictionary)

    board, _ = QuickAR.generate_grid_board()
    charuco_board, _ = QuickAR.generate_charuco_board()

    cam = QuickAR.Camera(0)

    camera_matrix_list = []
    dist_coeffs_list = []
    parameters = cv2.aruco.DetectorParameters_create()

    while cam.is_opened():
        frame = cam.get_frame()
        if frame is not None:
            if ret:
                # grayscale image
                gray = cam.convert_to_gray(frame)

                # Detect Aruco markers
                corners, ids, rejected_img_points = QuickAR.detect_markers(gray, aruco_dict, parameters)

                # Make sure markers were detected before continuing
                if ids is not None and corners is not None and len(ids) > 0 and len(corners) > 0 and len(corners) == len(
                        ids):
                    # The next if makes sure we see all matrixes in our board
                    if len(ids) == len(board.ids):
                        ret, camera_matrix, dist_coeffs = QuickAR.calibrate_from_board(gray, corners, board)
                        # ret, camera_matrix, dist_coeffs = calibrator.calibrate_from_aruco_board(gray, corners, ids, charuco_board)

                        # Print matrix and distortion coefficient to the console
                        print(f"camera matrix: {camera_matrix}  ::: dist coeffs: {dist_coeffs}")
                        camera_matrix_list.append(camera_matrix)
                        dist_coeffs_list.append(dist_coeffs)

            cv2.imshow("cam", frame)
        # Exit at the end of the video on the EOF key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.close()
    mean_camera_matrix = np.mean(camera_matrix_list, axis=0)
    mean_dist_coeffs = np.mean(dist_coeffs_list, axis=0)
    await QuickAR.save_calibration(mean_camera_matrix, mean_dist_coeffs)


if __name__ == "__main":
    print(__doc__)
    asyncio.run(main())
