#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse

"""
Project: QuickAR
Title: draw_image.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: This example demonstrates how to draw an image on the camera feed.
"""


async def main(args):
    desired_aruco_dictionary = args.aruco_dictionary
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])

    im_src = cv2.imread(args.image)

    if im_src is None:
        print("Could not open or find the image")
        exit(0)

    # Start the video stream
    cam = QuickAR.Camera(0)

    while cam.is_opened():
        frame = await cam.get_frame()
        if frame is not None:
            # Detect ArUco markers
            corners, ids = await QuickAR.detect_marker(frame, aruco_dictionary)
            if corners is not None:
                if len(corners) % 4 == 0:
                    between_frame = await QuickAR.image_between_markers(frame, corners, ids, im_src)
            else:
                between_frame = frame

            if corners is not None:
                multi_image_frame = await QuickAR.image_over_marker(frame, corners, im_src)
            else:
                multi_image_frame = frame

            if corners is not None:
                marker_frame = await QuickAR.draw_markers(frame, corners, ids)
            else:
                marker_frame = frame

            top = cv2.hconcat([frame, marker_frame])
            bottom = cv2.hconcat([multi_image_frame, between_frame])
            combined = cv2.vconcat([top, bottom])

            # Display
            cv2.imshow('frame', combined)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    parser = argparse.ArgumentParser(description='Example of renderer functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    parser.add_argument('--image',
                        type=str,
                        default='images/dog.png',
                        help='image to be used for inscription')

    arguments = parser.parse_args()
    asyncio.run(main(arguments))
