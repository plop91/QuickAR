import cv2
from .aruco_dict import ARUCO_DICT

"""
Title: detector.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


class Detector:
    """
    Detector class

    ----------

    Attributes

    -------

    Methods

    """

    def __init__(self, desired_aruco_dictionary):
        """

        :param desired_aruco_dictionary:
        """
        if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
            print("ArUCo tag type is not supported")
            exit(0)

        self.aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
        self.aruco_parameters = cv2.aruco.DetectorParameters_create()

    async def detect(self, frame):
        """
        detects aruco markers
        Args:
            frame:

        Returns:

        """
        return cv2.aruco.detectMarkers(frame, self.aruco_dictionary, parameters=self.aruco_parameters)

    @staticmethod
    async def draw_markers(corners, frame, ids):
        _frame = frame.copy()
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
                cv2.line(_frame, top_left, top_right, (0, 255, 0), 2)
                cv2.line(_frame, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(_frame, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(_frame, bottom_left, top_left, (0, 255, 0), 2)

                # Calculate and draw the center of the ArUco marker
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv2.circle(_frame, (center_x, center_y), 4, (0, 0, 255), -1)

                # Draw the ArUco marker ID on the video frame
                # The ID is always located at the top_left of the ArUco marker
                cv2.putText(_frame, str(marker_id),
                            (top_left[0], top_left[1] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
        return _frame
