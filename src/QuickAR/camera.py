import cv2

"""
Project: QuickAR
Title: camera.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: This class is used to interface with the camera.
"""

CAMERA_RESOLUTIONS = {
    "default": (640, 480),
    "640x480": (640, 480),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080),
    "2560X1440": (2560, 1440),
    "3840x2160": (3840, 2160),
    "480": (640, 480),
    "720": (1280, 720),
    "1080": (1920, 1080),
    "1440": (2560, 1440),
    "2160": (3840, 2160),

}


class Camera:
    """
    This class is used to interface with the camera.

    Attributes:
        _camera (cv2.VideoCapture): The camera object.
        output_resolution (tuple): The resolution of the camera.
        grayscale (bool): Whether the camera is in grayscale.

    Methods:
        __init__(self,camera_id, resolution="default", fps=30): Initializes the camera.
        static convert_to_gray(self, frame): Converts the frame to grayscale.
        static convert_resolution(self, resolution): Converts the resolution to a tuple.
        is_open(self): Checks if the camera is open.
        get_camera_resolution(self): Returns the resolution of the camera.
        get_camera_fps(self): Returns the frames per second of the camera.
        close(self): Closes the camera.
        async get_frame(self): Returns the current frame of the camera or None if there is no frame.
    """

    def __init__(self,
                 camera_id,
                 camera_resolution=CAMERA_RESOLUTIONS["default"],
                 fps=30,
                 grayscale=False,
                 output_resolution=None):
        """
        This function is used to initialize the camera.
        """
        self._camera = cv2.VideoCapture(camera_id)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_resolution[0])
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_resolution[1])
        self._camera.set(cv2.CAP_PROP_FPS, fps)

        if not self._camera.isOpened():
            raise Exception("Camera could not be opened.")

        self.grayscale = grayscale
        self.output_resolution = output_resolution

    def __del__(self):
        """
        This function is used to close the camera when the object is deleted.
        """
        self.close()

    @staticmethod
    def convert_to_gray(frame):
        """
        This function is used to convert the frame to gray.

        args:
            frame: The frame to convert to gray.

        returns:
            The frame in grayscale.
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def convert_resolution(frame, resolution=CAMERA_RESOLUTIONS["default"]):
        """
        This function is used to convert a resolution to a tuple.

        args:
            frame: The frame to convert.c
            resolution: The resolution to convert.

        returns:
            The frame in the specified resolution.
        """
        return cv2.resize(frame, resolution)

    def is_opened(self):
        """
        This function is used to check if the camera is opened.

        returns:
            True if the camera is opened, False otherwise.
        """
        return self._camera.isOpened()

    def get_camera_resolution(self):
        """
        This function is used to get the camera resolution.

        returns:
            The camera resolution.
        """
        return self._camera.get(cv2.CAP_PROP_FRAME_WIDTH), self._camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_camera_fps(self):
        """
        This function is used to get the camera fps.

        returns:
            The camera fps.
        """
        return self._camera.get(cv2.CAP_PROP_FPS)

    def close(self):
        """
        This function is used to close the camera.
        """
        self._camera.release()

    async def get_frame(self):
        """
        This function is used to get the frame from the camera.
        :return: The frame from the camera, or None if there is no frame.
        """
        ret, frame = self._camera.read()
        if ret:
            if self.output_resolution is not None:
                frame = cv2.resize(frame, self.output_resolution)
            if self.grayscale:
                frame = self.convert_to_gray(frame)
            return frame
        else:
            return None
