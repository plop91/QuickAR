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
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])

    im_src = cv2.imread(args.image)

    if im_src is None:
        print("Could not open or find the image")
        exit(0)

    # Start the video stream
    cam = cv2.VideoCapture(0)

    # resize camera resolution:
    # SD - 480p
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # ---------------------------------------- #
    # HD - 720p
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # ---------------------------------------- #
    # Full HD - 1080p
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # ---------------------------------------- #
    # 2K - 1440p
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
    # ---------------------------------------- #
    # 4K - 2160p
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    while cam.isOpened():
        ret, frame = cam.read()

        # Detect ArUco markers
        (corners, ids, rejected) = await QuickAR.detect(frame, aruco_dictionary)

        if len(corners) % 4 == 0:
            between_frame = await QuickAR.image_between_markers(frame, corners, ids, im_src)
        else:
            between_frame = frame

        multi_image_frame = await QuickAR.image_over_marker(frame, corners, im_src)

        marker_frame = await QuickAR.draw_markers(frame, corners, ids)

        top = cv2.hconcat([frame, marker_frame])
        bottom = cv2.hconcat([multi_image_frame, between_frame])
        all = cv2.vconcat([top, bottom])

        # Display
        cv2.imshow('frame', all)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
