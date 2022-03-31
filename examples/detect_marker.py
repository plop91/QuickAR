#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse

"""

"""


async def main():
    parser = argparse.ArgumentParser(description='Example of detector functions')
    parser.add_argument('--aruco_dictionary',
                        type=str,
                        default='DICT_ARUCO_ORIGINAL',
                        help='aruco dictionary to be used')
    args = parser.parse_args()

    desired_aruco_dictionary = args.aruco_dictionary
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])

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

        (corners, ids, rejected) = await QuickAR.detect(frame, aruco_dictionary)

        frame = await QuickAR.draw_markers(frame, corners, ids)

        # frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
