#!/usr/bin/env perl
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

sub sanitycheck {
	my ($dir, $file) = @_;

    print "Checking $dir\n";

	open(LIST_FILE, $file) or die "cant open $file";

	while (<LIST_FILE>) {
		chomp;
		
		next if /^\s*$/ or /^\#/;

		/^(\w+)/;
		my $lumpname = $1;

		my @files;

		if ($dir eq 'musics') {
			@files = glob("$dir/d_$lumpname*");
		} else {
			@files = glob("$dir/$lumpname*");
		}

		if (/done/ or /in dev/) {
			if (scalar @files <= 0) {
				print "$dir: files not found for $lumpname\n";
			}
		} else {
			if (scalar @files > 0) {
				print "$dir: files found for $lumpname\n";
			}
		}
	}

	close(LIST_FILE);
}

my $status_dir = "status";

sanitycheck 'sprites', "$status_dir/sprites_list";
sanitycheck 'patches', "$status_dir/patches_list";
sanitycheck 'flats', "$status_dir/flats_list";
sanitycheck 'graphics', "$status_dir/graphics_list";
sanitycheck 'sounds', "$status_dir/sounds_list";
#sanitycheck 'musics', "$status_dir/musics_list";

