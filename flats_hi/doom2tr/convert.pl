#!/usr/bin/perl

@files = glob("*.tga");

foreach(@files) {
	$pngfile = $_;
	$pngfile =~ s/tga$/png/;
	$cmd = "tgatoppm < $_ | pnmtopng > $pngfile";
	print "$cmd\n";
	`$cmd`;
}
