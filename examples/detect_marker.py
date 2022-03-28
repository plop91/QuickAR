#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse
"""

"""


async def main():
    parser = argparse.ArgumentParser(description='Example of renderer functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    parser.add_argument('--image',
                        type=str,
                        default='images/dog.png',
                        help='image to be used for inscription')

    args = parser.parse_args()

    desired_aruco_dictionary = args.aruco_dictionary
    detector = QuickAR.Detector(desired_aruco_dictionary)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        (corners, ids, rejected) = await detector.detect(frame)

        frame = await detector.draw_markers(corners, frame, ids)

        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
