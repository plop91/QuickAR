#!/usr/bin/env python3
import asyncio
import cv2
import os
import numpy as np
from detector import Detector
from generate_marker import MarkerGenerator


class Renderer():

    def apply_homography(self, im_src, pts_src, im_dst, pts_dst):
        # print(pts_src)
        h, status = cv2.findHomography(pts_src.astype(int), pts_dst.astype(int))
        return cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))


async def main():
    desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"
    detector = Detector(desired_aruco_dictionary)
    renderer = Renderer()
    generator = MarkerGenerator(desired_aruco_dictionary)

    marker = generator.generate(10)
    if not os.path.exists("images"):
        os.mkdir("images")
    cv2.imwrite("images/id10.png", marker)

    im_src = cv2.imread("images/id10.png")
    height, width, channels = im_src.shape
    pts_src = np.array([[0, 0], [height, 0], [height, width], [0, width]])

    # Start the video stream
    cap = cv2.VideoCapture(0)
    hom_frame = None

    while True:
        ret, frame = cap.read()

        # Detect ArUco markers
        (corners, ids, rejected) = await detector.detect(frame)

        await detector.draw_markers(corners, frame, ids)

        for corner in corners:
            hom_frame = renderer.apply_homography(im_src, pts_src, frame, corner.astype(int))
            frame = cv2.bitwise_or(hom_frame, frame)


        # Display
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())
