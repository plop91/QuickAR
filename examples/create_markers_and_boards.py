#!/usr/bin/env python3
import cv2
import os
import asyncio
import QuickAR
import argparse

"""
Project: QuickAR
Title: create_markers_and_boards.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: This script creates a set of markers and boards for use with the QuickAR SDK.
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
    aruco_dictionary = cv2.aruco.Dictionary_get(QuickAR.ARUCO_DICT[desired_aruco_dictionary])

    rows = []
    current_row = None
    for i in range(16):

        aruco_marker_id = i
        output_filename = f"images/marker_id{i}.png"
        marker = await QuickAR.generate_marker(aruco_dictionary, aruco_marker_id)
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
    cv2.imshow("ArUco Markers", output)

    board, board_img = await QuickAR.generate_grid_board(aruco_dictionary)
    cv2.imwrite("images/board.png", board_img)
    cv2.imshow("board_img", board_img)

    charuco_board, charuco_board_img = await \
        QuickAR.generate_charuco_board(aruco_dictionary)
    cv2.imwrite("images/charuco_board.png", charuco_board_img)
    cv2.imshow("charuco_board_img", charuco_board_img)

    cv2.waitKey(0)


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
