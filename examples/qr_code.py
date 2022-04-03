#!/usr/bin/env python3
import cv2
import asyncio
import QuickAR
import argparse

"""
Project: QuickAR
Title: qr_code.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description:
"""


async def main(args):
    # Start the video stream
    cam = QuickAR.Camera(0)

    while cam.is_opened():
        frame = await cam.get_frame()
        if frame is not None:
            # detect qr codes
            decoded_text, points = await QuickAR.detect_marker_qr(frame)

            print(decoded_text)

            # Display
            cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cam.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)

    parser = argparse.ArgumentParser(description='Example of qr code detection')

    arguments = parser.parse_args()
    asyncio.run(main(arguments))
