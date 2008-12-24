#!/usr/bin/env python
# 
# perform sanity check on assignments lists; make sure everything in
# the deutex tree is listed in the assignment lists
#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008
# Contributors to the Freedoom project.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the freedoom project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import glob
import re
import sys

# Find the file matching the given lump name:

def find_file(dirname, lumpname):

	if dirname == "musics":
		lumpname = "d_" + lumpname

	files = glob.glob("%s/%s*" % (dirname, lumpname))

	if len(files) > 0:
		return files[0]
	else:
		return None

# Perform sanity check on the given directory:

def sanity_check(dirname, filename):

	print "Checking %s" % dirname

	f = file(filename)

	for line in f:

		# Strip newline

		line = line[0:len(line)-1]

		# Ignore comments and empty lines

		if line == " " * len(line) or line[0] == "#":
			continue

		match = re.match(r'(\w+)', line)

		resource = match.group(1)

		# Find the file for this lump, if it exists

		filename = find_file(dirname, resource)

		# Is this resource supposed to be present? Check this
		# matches what is present.

		if re.search(r"(done|in dev)", line):
			if filename is None:
				print "%s: files not found for %s" % \
					(dirname, resource)
		else:
			if filename is None:
				print "%s: files found for %s" % \
					(dirname, resource)

	f.close()

status_dir = "status"

sections = {
	"sprites"  : "sprites_list",
	"patches"  : "patches_list",
	"flats"    : "flats_list",
	"graphics" : "graphics_list",
	"sounds"   : "sounds_list",
	"musics"   : "musics_list",
}

for section in sections.keys():
	sanity_check(section, "%s/%s" % (status_dir, sections[section]))

