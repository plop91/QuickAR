"""
Project: QuickAR
Title: container.py
Author: Ian Sodersjerna
Created: 3/31/2022
Description: Container class for holding the data for a single frame and wrapper functions for frame manipulation.
"""


class QuickARFrame:
    # TODO: is it easier to copy and update or create new container each time?

    frame = {
        'image': None,
        'corners': None,
        'ids': None,
        'aruco_dict': None,
        'boards': None,
        'flags': [],
    }

    def __init__(self, image=None, corners=None, ids=None, dictonary=None, boards=None):
        self.frame['image'] = image
        self.frame['corners'] = corners
        self.frame['ids'] = ids
        self.frame['dictionary'] = dictonary
        self.frame['boards'] = boards

    def __str__(self):
        return str(self.frame)

    def update(self, image=None, corners=None, ids=None, dictonary=None, boards=None):
        if image:
            self.frame['image'] = image
        if corners:
            self.frame['corners'] = corners
        if ids:
            self.frame['ids'] = ids
        if dictonary:
            self.frame['dictionary'] = dictonary
        if boards:
            self.frame['boards'] = boards

    @property
    def image(self):
        """
        Returns the image of the frame.
        Returns:

        """
        return self.frame['image']

    @property
    def corners(self):
        """
        Returns the corners of the boards found in the frame.
        Returns:

        """
        return self.frame['corners']

    @property
    def ids(self):
        """
        Returns the ids of the boards found in the frame.
        Returns:

        """
        return self.frame['ids']

    @property
    def dictionary(self):
        """
        Returns the dictionary used to find the boards in the frame.
        Returns:

        """
        return self.frame['dictionary']

    @property
    def boards(self):
        """
        Returns the boards found in the frame.
        Returns:

        """
        return self.frame['boards']


# TODO: add flag for if the frame is valid or not
def reframe(func):
    """
    Decorator for reframing the frame.
    """
    def wrapper():
        ret = func()
        print("refit the frame")

    return wrapper
