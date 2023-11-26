#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# endoom-tool - Display, split, cleanup and join ENDOOM lumps
#
# This script can be used to work with ENDOOM lumps. To see the ENDOOM lumps
# used by Freedoom the following make target can be used:
#   make display-endooms
# There are other tools to work with ENDOOM lumps, such as Playscii, but this
# tool can be helpful in some cases.
#
# If the display feature is used then it is important that the terminal support
# both Unicode and ANSI color codes. The former is almost certain, and ANSI
# color code support is likely, but try something like xterm if not.
#
# For information about the ENDOOM format:
#   https://doomwiki.org/wiki/ENDOOM
#
# Color letters, see in the foreground and background files after a split,
# relate to the Doom color numbers in the following way:
#
# Doom Color Number  Color Letter     Doom Color Number  Color Letter
# -----------------  ------------     -----------------  ------------
#                 0             .                     8             *
#                 1             b                     9             B
#                 2             g                    10             G
#                 3             c                    11             C
#                 4             r                    12             R
#                 5             m                    13             M
#                 6             y                    14             Y
#                 7             w                    15             W
#
# The upper case letters in the above correspond to bit 0x08 being set, which
# is extra bright when applied to the foreground, and blinking when applied to
# the background.
#
# Examples
#
#   The following examples assume that the script is run from the top level
#   build directory, but it should be possible to run it from anywhere.
#
#   To display (-d) the main ENDOOOM lump used by Freedoom:
#     scripts/endoom-tool -d lumps/endoom.lmp
#
#   To display (-d) a plain (-p) (no colors) version of the same ENDOOM lump:
#     scripts/endoom-tool -dp lumps/endoom.lmp
#
#   To display (-d) a randomly (-r) colored version of the same ENDOOM lump:
#     scripts/endoom-tool -dr lumps/endoom.lmp
#
#   To split (-s) the ENDOOM lump into three files (foreground, background
#   and text) into directory /tmp/endoom
#     scripts/endoom-tool -s /tmp/endoom lumps/endoom.lmp
#
#   To split (-s) the ENDOOM lump while also cleaning (-c) it so that unhelpful
#   color combinations are avoided.
#     scripts/endoom-tool -cs /tmp/endoom lumps/endoom.lmp
#
#   To join (-j) the /tmp/endoom directory created above to form a new ENDOOM
#   lump presumably after edits have been made to the files in that directory:
#     scripts/endoom-tool -j /tmp/endoom lumps/endoom-new.lmp
#
#   To join (-j) the /tmp/endoom directory created above but tolerate (-t)
#   missing files, truncated files and malformed files:
#     scripts/endoom-tool -tj /tmp/endoom lumps/endoom-new.lmp

# Imports

import argparse
import os
import struct
import sys
import zlib

# Globals. Alphabetical.

# Command line arguments.
args = {}

# The ENDOOM lump is code page 437:
#   https://en.wikipedia.org/wiki/Code_page_437
# It's ASCII with two additional sections that can be mapped to Unicode code
# points. The next two variables have to do with that mapping.

# For code page 437 the first 32 characters correspond to control characters in
# ASCII. One exception is that null (0) is mapped to space (32) for the first
# entry.
cp_437_to_uc_ord_low = (
    0x0020, 0x263A, 0x263B, 0x2665, 0x2666, 0x2663, 0x2660, 0x2022,  # 00 - 07
    0x25D8, 0x25CB, 0x25D9, 0x2642, 0x2640, 0x266A, 0x266B, 0x263C,  # 08 - 0f
    0x25BA, 0x25C4, 0x2195, 0x203C, 0x00B6, 0x00A7, 0x25AC, 0x21A8,  # 10 - 17
    0x2191, 0x2193, 0x2192, 0x2190, 0x221F, 0x2194, 0x25B2, 0x25BC)  # 18 - 1f

# For code page 437 the last 129 characters correspond to characters outside of
# the standard ASCII range.
cp_437_to_uc_ord_high = (                                   0x2302,  # 7f - 7f
    0x00C7, 0x00FC, 0x00E9, 0x00E2, 0x00E4, 0x00E0, 0x00E5, 0x00E7,  # 80 - 87
    0x00EA, 0x00EB, 0x00E8, 0x00EF, 0x00EE, 0x00EC, 0x00C4, 0x00C5,  # 88 - 8f
    0x00C9, 0x00E6, 0x00C6, 0x00F4, 0x00F6, 0x00F2, 0x00FB, 0x00F9,  # 90 - 97
    0x00FF, 0x00D6, 0x00DC, 0x00A2, 0x00A3, 0x00A5, 0x20A7, 0x0192,  # 98 - 9f
    0x00E1, 0x00ED, 0x00F3, 0x00FA, 0x00F1, 0x00D1, 0x00AA, 0x00BA,  # a0 - a7
    0x00BF, 0x2310, 0x00AC, 0x00BD, 0x00BC, 0x00A1, 0x00AB, 0x00BB,  # a8 - af
    0x2591, 0x2592, 0x2593, 0x2502, 0x2524, 0x2561, 0x2562, 0x2556,  # b0 - b7
    0x2555, 0x2563, 0x2551, 0x2557, 0x255D, 0x255C, 0x255B, 0x2510,  # b8 - bf
    0x2514, 0x2534, 0x252C, 0x251C, 0x2500, 0x253C, 0x255E, 0x255F,  # c0 - c7
    0x255A, 0x2554, 0x2569, 0x2566, 0x2560, 0x2550, 0x256C, 0x2567,  # c8 - cf
    0x2568, 0x2564, 0x2565, 0x2559, 0x2558, 0x2552, 0x2553, 0x256B,  # d0 - d7
    0x256A, 0x2518, 0x250C, 0x2588, 0x2584, 0x258C, 0x2590, 0x2580,  # d8 - df
    0x03B1, 0x00DF, 0x0393, 0x03C0, 0x03A3, 0x03C3, 0x00B5, 0x03C4,  # e0 - e7
    0x03A6, 0x0398, 0x03A9, 0x03B4, 0x221E, 0x03C6, 0x03B5, 0x2229,  # e8 - ef
    0x2261, 0x00B1, 0x2265, 0x2264, 0x2320, 0x2321, 0x00F7, 0x2248,  # f0 - f7
    0x00B0, 0x2219, 0x00B7, 0x221A, 0x207F, 0x00B2, 0x25A0, 0x00A0)  # f8 - ff

# With regard to the base color only 0 - 7 map from Doom color numbers to ANSI
# color numbers. The index in the array corresponds is a Doom color number.
doom_to_ansi_color_base = (0, 4, 2, 6, 1, 5, 3, 7)

# Similar to the above but map to a descriptive letter. To avoid duplicates '.'
# is used for black (and because its aesthetically close to black) and 'y' is
# used for brown (which is yellow when bright anyway).
doom_color_base_to_color_letter_base = ('.', 'b', 'g', 'c', 'r', 'm', 'y', 'w')

# Inverse tables for join. The following are inverted versions of some of the
# above for -j / --join which will be initialized later.

# Unicode code point to code page 437.
uc_to_cp_437_ord = {}

# From descriptive letter to Doom. This will be a sparse array since it's
# small, and because it's faster than an associative array.
color_letter_to_doom_color = []

# Get the ANSI color number. Returns a tuple (ansi_color, blink).
def get_ansi_color(doom_color, background):
    bright_blink    = 0x08 & doom_color # Bright or blinking.
    doom_color_base = 0x07 & doom_color
    ansi_color = doom_to_ansi_color_base[doom_color_base]
    if background:
        ansi_color += 40
    else:
        ansi_color += 30
    blink = False
    if bright_blink:
        if background:
            blink = True
        else:
            ansi_color += 60
    return (ansi_color, blink)

# Given a Doom color return a letter that describes it. Upper case is used for
# bright or blinking.
def get_color_letter(doom_color):
    bright_blink    = 0x08 & doom_color # Bright or blinking.
    doom_color_base = 0x07 & doom_color
    letter = doom_color_base_to_color_letter_base[doom_color_base]
    if bright_blink:
        if letter == ".":
            # Use "*" for an upper case ".".
            letter = "*"
        else:
            letter = letter.upper()
    return letter

# Initialize global variables.
def initialize():
    global color_letter_to_doom_color, uc_to_cp_437_ord

    # Currently only join needs initialization. Since it processes in the
    # reverse direction inverses of some tables will be created that would
    # otherwise not be needed.
    if args.join:
        # color_letter_to_doom_color will be a sparse array. The current lower case letters
        # in doom_color_base_to_color_letter_base include the highest possible letter ordinal. The
        # "+ 1" is because the array is zero based.
        color_letter_to_doom_color = [0] * (max([ord(l) for l in
            doom_color_base_to_color_letter_base]) + 1)

        for doom_color, color_letter in enumerate(doom_color_base_to_color_letter_base):
            # Lower case.
            color_letter_to_doom_color[ord(color_letter)] = doom_color

            # Upper case (bright / blinking).
            if color_letter == ".":
                color_letter_up = "*"
            else:
                color_letter_up = color_letter.upper()
            # For bright / blinking also set that bit.
            color_letter_to_doom_color[ord(color_letter_up)] = 8 | doom_color

        # Lower values.
        for cp_437_0, unicode in enumerate(cp_437_to_uc_ord_low):
            uc_to_cp_437_ord[unicode] = cp_437_0

        # Mid values are just ASCII.
        for ascii_char in range(32, 127):
            uc_to_cp_437_ord[ascii_char] = ascii_char

        # Upper values.
        for cp_437_127, unicode in enumerate(cp_437_to_uc_ord_high):
            uc_to_cp_437_ord[unicode] = cp_437_127 + 127

# Main entry point.
def main():
    parse_args()
    initialize()
    process_endooms()

# Open a file and return the handle. If args.tolerant then map exceptions to None
def open_file(file_name, mode):
    if os.path.exists(file_name) and not os.path.isfile(file_name):
        # The path existing but not as a file is probably not intended, even
        # in tolerant mode.
        print("File", file_name, "exists, but not as an ordinary file.",
              file=sys.stderr)
        sys.exit(1)
    try:
        file_hand = open(file_name, mode=mode)
    except OSError:
        if args.tolerant:
            file_hand = None
        else:
            print("Unable to open file", file_name, "with mode", mode, file=sys.stderr)
            sys.exit(1)
    return file_hand

# Parse the command line arguments and store the result in 'args'.
def parse_args():
    global args

    parser = argparse.ArgumentParser(
        description="Process the specified ENDOOM lumps.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler="resolve")

    command_group = parser.add_argument_group("Commands", "Specify exactly one command option")
    command_group_me = command_group.add_mutually_exclusive_group(required=True)

    # Commands. This is what the command does. Sorted alphabetically.

    command_group_me.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="Display command. Display the ENDOOM lump.")

    command_group_me.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Help. Show this help message and exit.")

    command_group_me.add_argument(
        "-j",
        "--join",
        metavar="JOIN-DIRECTORY",
        help="Join command. Join the directory previously created by --split " +
            "to form an ENDOOM lump.")

    command_group_me.add_argument(
        "-s",
        "--split",
        metavar="SPLIT-DIRECTORY",
        help="Split command. Split the ENDOOM lump into foreground, " +
            "background and text in the specified directory.")

    # Options that modify the command. Sorted alphabetically.

    option_group = parser.add_argument_group("Options", "Options that modify " +
                   "command behavior")

    option_group.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean. Make foreground equal to background for spaces, and convert " +
              "to space when foreground and background is the same color. " +
              "Recommended when the exact ENDOOM does not need to be maintained. " +
              "This option has no effect with -j, --join.")

    option_group.add_argument(
        "-p",
        "--plain",
        action="store_true",
        help="Plain. Disable all ANSI color effects. For -j, --join this means " +
             "to use white and black instead of what's in the foreground and " +
             "background files before any other color processing.")

    option_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Quiet. Disable some warnings and noise.")

    option_group.add_argument(
        "-r",
        "--random-colors",
        action="store_true",
        help="Random colors. Make the colors a hash of two bytes associated " +
             "with each character in order to make it easier to see " +
             "inconsistencies that are otherwise hidden.")

    option_group.add_argument(
        "-t",
        "--tolerant",
        action="store_true",
        help="Tolerate missing data. Missing files and data are considered " +
              "to be black spaces.")

    parser.add_argument(
        "endooms",
        metavar="ENDOOM",
        nargs="+",
        help="ENDOOM lump to process.")

    args = parser.parse_args()

    return args

# Process an ENDOOM lump.
def process_endoom(endoom_path):
    # If true then there were one or more nulls in the input.
    null_mapped_to_space = False
    nbsp_mapped_to_space = False
    black_space = b" \x00"
    try:
        read_write_binary = "wb" if args.join else "rb"
        endoom_hand = open_file(endoom_path, read_write_binary)
    except OSError:
        if args.tolerant:
            endoom_hand = None
        else:
            print("ENDOOM", endoom_path, "could not be opened for",
                ("write" if args.join else "read", ), ".", file=sys.stderr)
            sys.exit(1)
    if args.join or args.split:
        if args.split:
            os.makedirs(args.split, exist_ok=True)
        path = args.join if args.join else args.split
        read_write = "r" if args.join else "w"
        if not args.plain:
            fg_hand = open_file(path + "/foreground", read_write)
            bg_hand = open_file(path + "/background", read_write)
        text_hand = open_file(path + "/text", read_write)
    for row in range(25):
        if args.join:
            if not args.plain:
                fg_line = read_line_pad(fg_hand, "foreground", "W")
                bg_line = read_line_pad(bg_hand, "background", ".")
            text_line = read_line_pad(text_hand, "text"      , " ")
        for col in range(80):
            if args.join:
                if not args.plain:
                    fg_color_letter = fg_line[col]
                    fg_color_ord    = ord(fg_color_letter)
                    try:
                        fg_doom_color = color_letter_to_doom_color[fg_color_ord]
                    except KeyError:
                        if args.tolerant:
                            # Map unknown foreground to bright white.
                            fg_doom_color = 0x0f
                        else:
                            print("Unknown foreground character", fg_color_letter,
                                "in ENDOOM", endoom_path)

                    bg_color_letter = bg_line[col]
                    bg_color_ord = ord(bg_color_letter)
                    try:
                        bg_doom_color = color_letter_to_doom_color[bg_color_ord]
                    except KeyError:
                        if args.tolerant:
                            # Map unknown background to black.
                            bg_doom_color = 0x00
                        else:
                            print("Unknown background character", bg_color_letter,
                                "in ENDOOM", endoom_path)
                else:
                    # Use bright white on black for plain.
                    fg_doom_color = 0x0f
                    bg_doom_color = 0x00
                doom_color = (bg_doom_color << 4) | fg_doom_color

                text_uc_char = text_line[col]
                text_437_ord = uc_to_cp_437_ord[ord(text_uc_char)]

                two_bytes = struct.pack("BB", text_437_ord, doom_color)
            else:
                if endoom_hand:
                    two_bytes = endoom_hand.read(2)
                    if not two_bytes:
                        if not args.tolerant:
                            print("ENDOOM", endoom_path, "is less than 4000 bytes.",
                                file=sys.stderr)
                            sys.exit(1)
                        two_bytes = black_space
                else:
                    # It must be tolerant if we got here. Use a black space fo
                    #  the missing character.
                    two_bytes = black_space

                # Read the character and the color byte as integers and then
                # separate into foreground and backgound.
                text_437_ord, doom_color = struct.unpack("BB", two_bytes)
                fg_doom_color = 0x0f & doom_color
                bg_doom_color = 0x0f & (doom_color >> 4)
            bright = 0x08 & fg_doom_color
            blink  = 0x08 & bg_doom_color

            # Null (0) and space (32) look the same, but space is preferred
            # since it's used in most ENDOOM lumps, and because it is a
            # plain text character. The null will be mapped to space, and a
            # warning emitted to let the user know. Likewise with NBSP (255),
            # which is even less likely.
            if not text_437_ord:
                null_mapped_to_space = True
                text_437_ord = 32
            elif text_437_ord == 255:
                nbsp_mapped_to_space = True
                text_437_ord = 32

            if text_437_ord <= 31:
                text_uc_ord = cp_437_to_uc_ord_low[text_437_ord]
            elif text_437_ord >= 127:
                text_uc_ord = cp_437_to_uc_ord_high[text_437_ord - 127]
            else:
                # ASCII, no need to translate.
                text_uc_ord = text_437_ord

            text_uc_char = chr(text_uc_ord)

            # Ideally all visibly distinct characters would have a single
            # unique clean representation with a few exceptions (spaces and full
            # block characters that are the same color can look identical, but
            # have different intent, so they are not interchangeable).
            #
            # Basically if it only displays one color then it can only have one
            # color. If it looks like a space then it becomes a space.
            if args.clean:
                if text_uc_ord == 32 and (not blink):
                    # For spaces the foreground may as well be the same
                    # color as the background. Avoid changing blinking spaces
                    # since the higher order bit has a different meaning in the
                    # foreground.
                    if fg_doom_color != bg_doom_color:
                        fg_doom_color = bg_doom_color
                elif text_uc_ord == 0x2588 and (not bright) and (not blink):
                    # The full block character (U+2588) is the opposite of
                    # space in that only the foreground is visible, not the
                    # background. Use the foreground.
                    if bg_doom_color != fg_doom_color:
                        bg_doom_color = fg_doom_color
                elif (fg_doom_color == bg_doom_color) and (not bright):
                    # For non-spaces the foreground and background should
                    # not be exactly the same color, which is only possible
                    # if the bright / blink bit is not set. Note that we
                    # only need to check that bit for the foreground since
                    # otherwise they would not be equal. Map to space.
                    text_uc_ord = 32
                    text_uc_char = chr(text_uc_ord)

            # Map colors to a hash of the two bytes that make up the character.
            # This can be helpful for seeing otherwise hidden formatting.
            if args.random_colors:
                # For the foreground highlighting is allowed, so 16
                # possibilities. Avoid blinking for the background, so
                # there are only 8 allowed colors.
                #
                # The "+ b'X'" is so that they have unrelated hashes.
                #
                # The 13 and 4 offset is so that black spaces are
                # mapped to black spaces.
                fg_doom_color = (zlib.crc32(two_bytes)        - 13) % 16
                bg_doom_color = (zlib.crc32(two_bytes + b'X') -  4) %  8

                # It's nice if they are different, so increment the
                # background if they are the same. However, if they are
                # just black spaces then keep that.
                if bg_doom_color == fg_doom_color and bg_doom_color:
                    bg_doom_color += 1
                    if bg_doom_color >= 8:
                        bg_doom_color = 0

            # The remaining lines in this method mostly have to do with
            # output and error handling.

            if args.join:
                endoom_hand.write(two_bytes)
            elif args.split:
                if not args.plain:
                    fg_letter = get_color_letter(fg_doom_color)
                    fg_hand.write(fg_letter)
                    bg_letter = get_color_letter(bg_doom_color)
                    bg_hand.write(bg_letter)
                text_hand.write(text_uc_char)
            elif args.display:
                if args.plain:
                    print(text_uc_char, end="")
                else:
                    fg_ansi_color, _     = get_ansi_color(fg_doom_color, False)
                    bg_ansi_color, blink = get_ansi_color(bg_doom_color, True)

                    # Handle blinking by setting and then unsetting.
                    if blink:
                        print("\033[5m", end="")
                    print("\033[%d;%dm%c" % (fg_ansi_color, bg_ansi_color, text_uc_char), end="")
                    if blink:
                        print("\033[0m", end="")
        if args.split:
            if not args.plain:
                fg_hand.write("\n")
                bg_hand.write("\n")
            text_hand.write("\n")
        elif args.display:
            if args.plain:
                print()
            else:
                print("\033[0m")
    if not args.quiet:
        if null_mapped_to_space:
            print("WARNING: One or more null (0) characters mapped to " +
                "space (32) for", endoom_path, file=sys.stderr)
        if nbsp_mapped_to_space:
            print("WARNING: One or more NBSP (255) characters mapped to " +
                "space (32) for", endoom_path, file=sys.stderr)
    if endoom_hand:
        if (not args.join) and (endoom_hand.read(1) and not args.tolerant):
            print("ENDOOM", endoom_path, "is more than 4000 bytes.", file=sys.stderr)
            sys.exit(1)
        endoom_hand.close()
    if args.split or args.join:
        if fg_hand:
            fg_hand.close()
        if bg_hand:
            bg_hand.close()
        if text_hand:
            text_hand.close()

# Process multiple ENDOOM lumps.
def process_endooms():
    for endoom_path in args.endooms:
        process_endoom(endoom_path)

# Read a line. Pad it if needed and allowed.
def read_line_pad(file_hand, file_type, pad_char):
    if not file_hand:
        # The space characters will be appended below. It must be tolerant
        # if we got here.
        file_line = ""
    else:
        file_line = file_hand.readline()
        # Strip the trailing newline, if any.
        if file_line and (file_line[-1] == "\n"):
            file_line = file_line[0:-1]
    if len(file_line) != 80 and not args.tolerant:
        print("For join directory", args.join, "file type", file_type,
            "has a line that is not 80 characters. line=", file_line,
            file=sys.stderr)
        sys.exit(1)
    if len(file_line) < 80:
        file_line += pad_char * (80 - len(file_line))
    return file_line

# So that this script may be accessed as a module.
if __name__ == "__main__":
    main()
