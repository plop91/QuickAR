import cv2
import numpy as np

"""
Title: renderer.py
Author: Ian Sodersjerna
Created: 3/20/2022

Worklog: 

3/20/2022:
"""


class Renderer:
    """
    Renderer class

    ----------

    Attributes

    -------

    Methods
    image_over_marker(self, corners, frame, image)

    image_between_markers(self, corners, ids, frame, image)

    apply_homography(tl, tr, br, bl, image, img)
    """

    async def image_over_marker(self, corners, frame, image):
        """
        inscribe image over marker
        :param corners: list of corners to be inscribed upon
        :param frame: frame to be drawn upon
        :param image: image to be drawn to frame
        :return: inscribed frame
        """
        img = frame.copy()
        for bbox in corners:
            tl = bbox[0][0][0], bbox[0][0][1]
            tr = bbox[0][1][0], bbox[0][1][1]
            br = bbox[0][2][0], bbox[0][2][1]
            bl = bbox[0][3][0], bbox[0][3][1]
            img = await self.apply_homography(tl, tr, br, bl, image, img)
        return img

    async def image_between_markers(self, corners, ids, frame, image):
        """
        inscribe image between markers, corners are assigned via id in ascending order following the pattern top-left,
        top-right, bottom-right, bottom-left
        :param corners: list of corners of markers, length must be multiple of 4
        :param ids: list of ids of corners, length must be multiple of 4
        :param frame: frame to be drawn upon
        :param image: image to be drawn to frame
        :return: inscribed frame
        """
        if len(corners) == 0:
            return frame
        elif len(corners) % 4 != 0:
            raise ValueError("corners must come in sets of 4")
        zipped = zip(ids, corners)
        zlist = (list(zipped))
        zlist.sort()
        _ids, _corners = zip(*zlist)
        img = frame.copy()
        for corner_set in np.array_split(_corners, len(_corners) / 4):
            tl = corner_set[0][0][0][0], corner_set[0][0][0][1]
            tr = corner_set[1][0][1][0], corner_set[1][0][1][1]
            br = corner_set[2][0][2][0], corner_set[2][0][2][1]
            bl = corner_set[3][0][3][0], corner_set[3][0][3][1]
            img = await self.apply_homography(tl, tr, br, bl, image, img)
        return img

    @staticmethod
    async def apply_homography(tl, tr, br, bl, image, img):
        """
        Applies homography to img

        :param tl: top left point of image
        :param tr: top right point of image
        :param br: bottom right point of image
        :param bl: bottom left point of image
        :param image: image to written over img
        :param img: image to be written on
        :return: img with homography image applied to it
        """
        h, w, c = image.shape
        pts1 = np.array([tl, tr, br, bl])
        pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        matrix, _ = cv2.findHomography(pts2, pts1)
        imgout = cv2.warpPerspective(image, matrix, (img.shape[1], img.shape[0]))
        cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
        img = img + imgout
        return img
