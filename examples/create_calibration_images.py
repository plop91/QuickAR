import cv2
import os
import QuickAR
import asyncio
import argparse

"""
Project: QuickAR
Title: create_calibration_images.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description:
"""


async def main(args):
    cam = QuickAR.Camera(0, camera_resolution=QuickAR.CAMERA_RESOLUTIONS["2k"])

    files = os.listdir("images")
    image_files = [f for f in files if f.endswith(".png")]
    training_image_files = [f for f in image_files if f.startswith("training")]

    img_counter = len(training_image_files)

    while cam.is_opened():
        frame = await cam.get_frame()
        if frame is not None:
            cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            corners, ids = await QuickAR.detect_marker(frame)
            if len(corners) == 35:
                img_name = f"images/training_{img_counter}.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
            else:
                print("Not enough markers detected!")

    cam.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(__doc__)

    parser = argparse.ArgumentParser(description='Example of qr code detection')

    arguments = parser.parse_args()

    asyncio.run(main(arguments))
