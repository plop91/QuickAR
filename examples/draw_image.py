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
    renderer = QuickAR.Renderer()

    im_src = cv2.imread(args.image)

    if im_src is None:
        print("Could not open or find the image")
        exit(0)

    # Start the video stream
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detect ArUco markers
        (corners, ids, rejected) = await detector.detect(frame)

        if len(corners) % 4 == 0:
            between_frame = await renderer.image_between_markers(corners, ids, frame, im_src)
        else:
            between_frame = frame

        multi_image_frame = await renderer.image_over_marker(corners, frame, im_src)

        marker_frame = await detector.draw_markers(corners, frame, ids)

        top = cv2.hconcat([frame, marker_frame])
        bottom = cv2.hconcat([multi_image_frame, between_frame])
        all = cv2.vconcat([top, bottom])

        # Display
        cv2.imshow('frame', all)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
