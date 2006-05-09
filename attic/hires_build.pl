#!/usr/bin/perl
#
# Convert all pngs to tgas 
#

# clear out old tgas

`rm hires/*.tga`;

# get list of input files

@files = (glob ("flats_hi/*.png"), glob ("patches_hi/*.png"));

foreach(@files) {
	$tgafile = $_;
	$tgafile =~ s/.*\///;
	$tgafile =~ s/png$/tga/;

	$cmd = "pngtopnm < $_ | ppmtotga > hires/$tgafile 2>/dev/null";
	#print "$cmd\n";
	`$cmd`;
}

