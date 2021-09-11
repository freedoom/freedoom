#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

import re

from PIL import Image


def get_image_dimensions(filename):
    """Get image dimensions w x h

    Args:
      filename: filename of the image
    """
    with Image.open(filename) as img:
        width, height = img.size
    return (width, height)


if __name__ == "__main__":
    import sys

    x, y = get_image_dimensions(sys.argv[1])
    string = "%i %i" % (x, y)
    sys.stdout.write(string)
