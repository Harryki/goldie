# -*- coding: utf-8 -*-
"""
File: face.py
Description: Face model.
"""


class Face():
    """Face Model for each face."""

    def __init__(self):
        self.name = None

    def set_name(self, name):
        """Set the name for the face."""
        self.name = name