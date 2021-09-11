#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2017 Martin Miller, Nick Zatkovich
# https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil

from PIL import Image, ImageColor, ImageOps


def image_tint(image, tint=None):
    if tint is None:
        return image
    if image.mode not in ["RGB", "RGBA"]:
        image = image.convert("RGBA")

    tr, tg, tb = ImageColor.getrgb(tint)
    tl = ImageColor.getcolor(tint, "L")  # tint color's overall luminosity
    if not tl:
        tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(
        lambda tv: tv / tl, (tr, tg, tb)
    )  # per component adjustments

    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (
        tuple(map(lambda lr: int(lr * sr + 0.5), range(256)))
        + tuple(map(lambda lg: int(lg * sg + 0.5), range(256)))
        + tuple(map(lambda lb: int(lb * sb + 0.5), range(256)))
    )
    l = ImageOps.grayscale(image)  # 8-bit luminosity version of whole image
    if Image.getmodebands(image.mode) < 4:
        merge_args = (image.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of image's alpha layer
        a = Image.new("L", image.size)
        a.putdata(image.getdata(3))
        merge_args = (image.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += tuple(range(256))  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)


def main(input_image_path, tintcolor, result_image_path):
    image = Image.open(input_image_path)

    image.load()

    result = image_tint(image, tintcolor)
    if os.path.exists(result_image_path):  # delete any previous result file
        os.remove(result_image_path)
    result.save(result_image_path)  # file name's extension determines format


if __name__ == "__main__":
    import os
    import sys

    main(sys.argv[1], sys.argv[2], sys.argv[3])
