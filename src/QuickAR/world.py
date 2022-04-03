import math

"""
Project: QuickAR
Title: world.py
Author: Ian Sodersjerna
Created: 4/2/2022
Description: 
"""


class World:
    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return self._objects
