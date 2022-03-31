import cv2


def Camera(camera_id):
    """
    Get camera by id.
    """
    return cv2.VideoCapture(camera_id)
