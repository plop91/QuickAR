#!/usr/bin/env python3


import cv2
import numpy as np
from aruco_dict import ARUCO_DICT


class MarkerGenerator:

    def __init__(self, desired_aruco_dictionary):
        if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
            print("ArUCo tag type is not supported")
            exit(0)

        self.aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])

    def generate(self, aruco_marker_id):
        # Create the ArUco marker
        marker = np.zeros((300, 300, 1), dtype="uint8")
        cv2.aruco.drawMarker(self.aruco_dictionary, aruco_marker_id, 300, marker, 1)
        return marker


def main():
    """
    Main method of the program.
    """
    import os

    if not os.path.exists("images"):
        os.mkdir("images")

    desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"
    rows = []
    current_row = None
    for i in range(16):

        aruco_marker_id = i+1
        output_filename = f"images/id{i+1}.png"
        generator = MarkerGenerator(desired_aruco_dictionary)
        marker = generator.generate(aruco_marker_id, output_filename)
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
    main()
