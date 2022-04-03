#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse

"""
Project: QuickAR
Title: estimate_pose_marker.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description:
"""


async def main(args):
    desired_aruco_dictionary = args.aruco_dictionary
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])
    camera_matrix, dist_coeffs = await QuickAR.load_calibration()
    # camera_matrix, dist_coeffs = await QuickAR.create_zero_calibration()

    cam = QuickAR.Camera(0)

    while cam.is_opened():
        frame = await cam.get_frame()
        if frame is not None:
            # detect markers
            corners, ids = await QuickAR.detect_marker(frame, aruco_dictionary)
            if corners is not None:
                rvecs, tvecs = await QuickAR.pose_marker(corners, 0.02, camera_matrix, dist_coeffs)
                frame = await QuickAR.draw_axis_marker(frame, rvecs, tvecs, camera_matrix, dist_coeffs)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    parser = argparse.ArgumentParser(description='Estimate pose of a marker')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    arguments = parser.parse_args()
    asyncio.run(main(arguments))
