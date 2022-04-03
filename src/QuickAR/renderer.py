import cv2
import numpy as np

"""
Project: QuickAR
Title: renderer.py
Author: Ian Sodersjerna
Created: 3/20/2022
Description: This class is used to render images or markers to an image.
"""


async def draw_markers(frame, corners, ids):
    """
    Draws markers on frame.

    args:
        frame: frame to be drawn upon
        corners: list of corners of markers
        ids: list of ids of corners

    returns:
        frame: frame with markers drawn
    """
    if frame is None or corners is None or ids is None:
        return frame

    _frame = cv2.aruco.drawDetectedMarkers(
        image=frame,
        corners=corners)

    return _frame


async def draw_ids_on_marker(frame, corners, ids):
    """
    Draws id on marker.

    args:
        frame: frame to be drawn upon
        corners: list of corners of markers
        ids: list of ids of corners

    returns:
        frame: frame with id inscribed
    """
    if frame is None or corners is None or ids is None:
        return frame
    elif len(ids) != len(corners):
        raise ValueError("Length of ids and corners must be equal")
    _frame = frame.copy()
    for (_corner, _id) in zip(corners, ids):
        _frame = await draw_text_on_marker(_frame, _corner, _id[0])
    return _frame


async def draw_text_on_marker(frame, corner, text):
    if frame is None or corner is None or text is None:
        return frame
    _frame = frame.copy()

    # Extract the marker corners
    corners = corner.reshape((4, 2))
    (top_left, top_right, bottom_right, bottom_left) = corners

    # Convert the (x,y) coordinate pairs to integers
    top_left = (int(top_left[0]), int(top_left[1]))

    # Draw the ArUco marker ID on the video frame
    # The ID is always located at the top_left of the ArUco marker
    cv2.putText(_frame, str(text),
                (top_left[0], top_left[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    return _frame


async def draw_axis_marker(frame, rvec, tvec, matrix_coefficients, distortion_coefficients):
    """
    Draws axis on marker.
    #NOTE: This function is not currently functional

    args:
        frame: frame to be drawn upon
        rvec: rotation vector
        tvec: translation vector
        matrix_coefficients: matrix coefficients
        distortion_coefficients: distortion coefficients
    """
    if rvec is None or tvec is None or matrix_coefficients is None or distortion_coefficients is None:
        print("test")
        return frame
    for i in range(len(rvec)):
        _frame = cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec[i], tvec[i], 0.01)
    return _frame


async def image_over_marker(frame, corners, image):
    """
    Inscribe image over marker

    args:
        frame: frame to be drawn upon
        corners: list of corners to be inscribed upon
        image: image to be drawn to frame

    returns:
        frame: frame with image inscribed
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

    args:
        frame: frame to be drawn upon
        corners: list of corners of markers, length must be multiple of 4
        ids: list of ids of corners, length must be multiple of 4
        image: image to be drawn to frame

    returns:
        frame: frame with image inscribed
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

    args:
        frame: frame to be drawn on
        tl: top left point of image
        tr: top right point of image
        br: bottom right point of image
        bl: bottom left point of image
        image: image to written over frame

    returns:
        frame: frame with image inscribed
    """
    h, w, c = image.shape
    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    _image = cv2.warpPerspective(image, matrix, (frame.shape[1], frame.shape[0]))
    cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
    frame = frame + _image
    return frame
