import cv2
import numpy as np

"""
Title: renderer.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


async def draw_markers(frame, corners, ids):
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


async def draw_axis_marker(frame, corners, matrix_coefficients, distortion_coefficients):
    for i in range(len(corners)):
        rvec, tvec, marker_points = cv2.aruco.estimatePoseSingleMarkers(corners[i],
                                                                        0.02,
                                                                        matrix_coefficients,
                                                                        distortion_coefficients)
        (rvec - tvec).any()  # get rid of that nasty numpy value array error
        cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)  # Draw axis


async def image_over_marker(frame, corners, image):
    """
    Inscribe image over marker

    :param frame: frame to be drawn upon
    :param corners: list of corners to be inscribed upon
    :param image: image to be drawn to frame
    :return: inscribed frame
    """
    _frame = frame.copy()
    for bbox in corners:
        tl = bbox[0][0][0], bbox[0][0][1]
        tr = bbox[0][1][0], bbox[0][1][1]
        br = bbox[0][2][0], bbox[0][2][1]
        bl = bbox[0][3][0], bbox[0][3][1]
        _frame = await apply_homography(_frame, tl, tr, br, bl, image)
    return _frame


async def image_between_markers(frame, corners, ids, image):
    """
    Inscribe image between markers, corners are assigned via id in ascending order following the pattern top-left,
    top-right, bottom-right, bottom-left.

    :param frame: frame to be drawn upon
    :param corners: list of corners of markers, length must be multiple of 4
    :param ids: list of ids of corners, length must be multiple of 4
    :param image: image to be drawn to frame
    :return: inscribed frame
    """
    if len(corners) < 4:
        return frame
    elif len(corners) % 4 != 0:
        raise ValueError("corners must come in sets of 4")
    zipped = zip(ids, corners)
    zlist = (list(zipped))
    zlist.sort()
    _ids, _corners = zip(*zlist)
    _frame = frame.copy()
    for corner_set in np.array_split(_corners, len(_corners) / 4):
        tl = corner_set[0][0][0][0], corner_set[0][0][0][1]
        tr = corner_set[1][0][1][0], corner_set[1][0][1][1]
        br = corner_set[2][0][2][0], corner_set[2][0][2][1]
        bl = corner_set[3][0][3][0], corner_set[3][0][3][1]
        _frame = await apply_homography(_frame, tl, tr, br, bl, image)
    return _frame


async def apply_homography(frame, tl, tr, br, bl, image):
    """
    Applies homography to img.

    :param frame: frame to be drawn on
    :param tl: top left point of image
    :param tr: top right point of image
    :param br: bottom right point of image
    :param bl: bottom left point of image
    :param image: image to written over img
    :return: img with homography image applied to it
    """
    h, w, c = image.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    _image = cv2.warpPerspective(image, matrix, (frame.shape[1], frame.shape[0]))
    cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
    frame = frame + _image
    return frame
