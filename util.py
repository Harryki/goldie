# -*- coding: utf-8 -*-
"""
File: util.py
Description: util module.
"""

import os.path
import config
from PIL import Image, ExifTags

try:
    import cognitive_face as CF
except ImportError:
    import sys

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, ROOT_DIR)
    import cognitive_face as CF


def init_subscription():
    CF.Key.set(config.FACE_API_KEY)
    CF.BaseUrl.set(config.BASE_URL)


def straighten_image(imagePath):
    try:
        dir_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(dir_path, imagePath)

        image = Image.open(file_path)
        image.show()
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(file_path)
        image.close()

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

