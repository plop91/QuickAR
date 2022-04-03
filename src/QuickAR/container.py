"""
Project: QuickAR
Title: container.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: Container class for holding the data for a single frame and wrapper functions for frame manipulation.
"""


# TODO: Add support for multiple container types

class QuickARFrame:
    # TODO: is it easier to copy and update or create new container each time?

    _frame = {
        'image': None,
        'corners': None,
        'ids': None,
        'flags': [],
    }

    def __init__(self, image=None, corners=None, ids=None, dictionary=None):
        self._frame['image'] = image
        self._frame['corners'] = corners
        self._frame['ids'] = ids
        self._frame['dictionary'] = dictionary

    def __str__(self):
        return str(self._frame)

    def update(self, image=None, corners=None, ids=None, dictionary=None):
        if image:
            self._frame['image'] = image
        if corners:
            self._frame['corners'] = corners
        if ids:
            self._frame['ids'] = ids
        if dictionary:
            self._frame['dictionary'] = dictionary

    @property
    def image(self):
        """
        Returns the image of the frame.
        Returns:

        """
        return self._frame['image']

    @property
    def corners(self):
        """
        Returns the corners of the boards found in the frame.
        Returns:

        """
        return self._frame['corners']

    @property
    def ids(self):
        """
        Returns the ids of the boards found in the frame.
        Returns:

        """
        return self._frame['ids']

    @property
    def dictionary(self):
        """
        Returns the dictionary used to find the boards in the frame.
        Returns:

        """
        return self._frame['dictionary']

    @property
    def boards(self):
        """
        Returns the boards found in the frame.
        Returns:

        """
        return self._frame['boards']


class QuickARConfig:
    _config = {
        'camera_matrix': None,
        'dist_coeffs': None,
    }


# TODO: add flag for if the frame is valid or not
def reframe(func):
    """
    Decorator for re-framing the frame.
    """

    def wrapper():
        ret = func()
        print("refit the frame")

    return wrapper
