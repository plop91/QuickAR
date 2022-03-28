#!/usr/bin/env python3
import cv2
import os
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

    args = parser.parse_args()

    if not os.path.exists("images"):
        os.mkdir("images")

    desired_aruco_dictionary = args.aruco_dictionary
    rows = []
    current_row = None
    for i in range(16):

        aruco_marker_id = i
        output_filename = f"images/id{i}.png"
        generator = QuickAR.MarkerGenerator(desired_aruco_dictionary)
        marker = generator.generate_marker(aruco_marker_id)
        cv2.imwrite(output_filename, marker)
        if current_row is None:
            current_row = marker
        elif i % 4 == 0:
            rows.append(current_row)
            current_row = marker
        elif i == 15:
            current_row = cv2.hconcat([current_row, marker])
            rows.append(current_row)
        else:
            current_row = cv2.hconcat([current_row, marker])

    output = cv2.vconcat(rows)
    cv2.imshow("ArUco Marker", output)
    cv2.waitKey(0)


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
