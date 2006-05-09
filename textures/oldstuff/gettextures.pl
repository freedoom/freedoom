#!/usr/bin/perl

my @list;

while (<>) {
	chomp;

	next if !/^[A-Z]/;

	my ($texturename) = /^([A-Z0-9]*)/;

	push @list, $texturename;
}

foreach(sort @list) {
	print "$_\n";
}
