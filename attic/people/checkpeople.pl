#!/usr/bin/perl

use strict;

while (<>) {
	chomp;
	`grep $_ CREDITS`;
	print "$_ not found\n" if $?;
}

