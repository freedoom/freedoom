#/usr/bin/env python

# SPDX-License-Identifier: BSD-3-Clause

from PIL import Image

import sys
import os

img = Image.open(sys.argv[1])
img.load()
img2 = img.rotate(int(sys.argv[2]), None, True)
img2.crop() 
if os.path.exists(sys.argv[3]):  # delete any previous result file
	os.remove(sys.argv[3])
img2.save(sys.argv[3])
