#!/usr/bin/perl
#
# get dimensions of all patches
# run file -L patches/*.gif and pipe through this

while (<>) {
	chomp;
	s/^(.*)\.gif.*\s(\d+)\ x\ (\d+)$/$1\ $2\ $3/;
	print "$_\n";
}

