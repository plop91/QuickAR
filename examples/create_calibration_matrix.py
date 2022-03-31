#!/usr/bin/env python3
import numpy as np
import cv2
import QuickAR
import asyncio
"""

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

    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

    camera_matrix_list = []
    dist_coeffs_list = []

    while cam.isOpened():
        ret, frame = cam.read()
        frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA)
        if ret:
            # grayscale image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            parameters = cv2.aruco.DetectorParameters_create()

            # Detect Aruco markers
            corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

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
    mean_camera_matrix = np.mean(camera_matrix_list, axis=0)
    mean_dist_coeffs = np.mean(dist_coeffs_list, axis=0)
    await QuickAR.save_calibration(mean_camera_matrix, mean_dist_coeffs)


if __name__ == "__main":
    print(__doc__)
    asyncio.run(main())
