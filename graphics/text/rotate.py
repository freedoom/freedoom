#/usr/bin/env python

# SPDX-License-Identifier: BSD-3-Clause

from PIL import Image

import sys
import os

img = Image.open(sys.argv[1])
img.load()
angle = int(sys.argv[2])
if angle % 90 == 0:
    if angle == 90 or angle == -270:
        method = Image.ROTATE_90
    elif abs(angle) == 180:
        method = Image.ROTATE_180
    else:
        method = Image.ROTATE_270
    img2 = img.transpose(method)
else:
    img2 = img.rotate(int(sys.argv[2]), 0, True)
    img2 = img2.crop()

if os.path.exists(sys.argv[3]):  # delete any previous result file
	os.remove(sys.argv[3])
img2.save(sys.argv[3])
