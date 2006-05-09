#!/usr/bin/perl

use strict;

my %people = {};

foreach (glob("*/*.*")) {
	my $pointto = readlink($_);

	if (!$pointto) {
		print STDERR "$_ not a link\n";
	} else {
		my ($person) = ($pointto =~ /^(\w+)\//);
		$people{$person} = 1 if $person;
	}
}

foreach (keys %people) {
	print "$_\n";
}

