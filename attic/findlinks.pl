#!/usr/bin/perl

sub do_dir {
	my ($dir, $extn) = @_;
	my @files = glob("$dir/*.$extn");
	my %spriteowners = {};

	print "[$dir]\n\n";

	foreach (@files) {
		my $link = readlink ($_);

		next if (!$link);

		my ($owner) = $link;
		my $base = $_;

		$base =~ s/^\w*\///;
		$base =~ s/\.$extn//;
		$owner =~ s/\/.*$//;

		print "$base: $owner\n";
	}

	print "\n";
}

do_dir "graphics", "gif";
do_dir "levels", "wad";
do_dir "sprites", "gif";
do_dir "flats", "gif";
do_dir "patches", "gif";
do_dir "lumps", "lmp";

