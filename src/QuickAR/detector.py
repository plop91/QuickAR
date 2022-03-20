#!/usr/bin/env python3

import asyncio
import cv2
import numpy as np
from aruco_dict import ARUCO_DICT


class Detector:

    def __init__(self, desired_aruco_dictionary):
        # Check that we have a valid ArUco marker
        if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
            print("ArUCo tag type is not supported")
            exit(0)

        # Load the ArUco dictionary
        print("[INFO] detecting '{}' markers...".format(desired_aruco_dictionary))
        self.aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
        self.aruco_parameters = cv2.aruco.DetectorParameters_create()

    async def detect(self, frame):
        return cv2.aruco.detectMarkers(frame, self.aruco_dictionary, parameters=self.aruco_parameters)

    async def draw_markers(self, corners, frame, ids):
        # Check that at least one ArUco marker was detected
        if len(corners) > 0:
            # Flatten the ArUco IDs list
            ids = ids.flatten()

            # Loop over the detected ArUco corners
            for (marker_corner, marker_id) in zip(corners, ids):
                # Extract the marker corners
                corners = marker_corner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                # Convert the (x,y) coordinate pairs to integers
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))

                # Draw the bounding box of the ArUco detection
                cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
                cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

                # Calculate and draw the center of the ArUco marker
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

                # Draw the ArUco marker ID on the video frame
                # The ID is always located at the top_left of the ArUco marker
                cv2.putText(frame, str(marker_id),
                            (top_left[0], top_left[1] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)


async def main():
    desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"
    detector = Detector(desired_aruco_dictionary)

    # Start the video stream
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detect ArUco markers
        (corners, ids, rejected) = await detector.detect(frame)

        await detector.draw_markers(corners, frame, ids)

        # Display
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    asyncio.run(main())
