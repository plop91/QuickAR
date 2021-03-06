#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse

"""
Project: QuickAR
Title: detect_marker.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: Detects markers in a video stream.
"""


async def main(args):

    desired_aruco_dictionary = args.aruco_dictionary
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])

    cam = QuickAR.Camera(0)

    while cam.is_opened():
        frame = await cam.get_frame()
        if frame is not None:
            # detect markers
            corners, ids = await QuickAR.detect_marker(frame, aruco_dictionary)
            # draw the markers
            frame = await QuickAR.draw_markers(frame, corners, ids)
            # draw id numbers
            frame = await QuickAR.draw_ids_on_marker(frame, corners, ids)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    parser = argparse.ArgumentParser(description='Example of detector functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    arguments = parser.parse_args()
    asyncio.run(main(arguments))
