package Time::DaysInMonth;

use Carp;

require 5.000;

@ISA = qw(Exporter);
@EXPORT = qw(days_in is_leap);
@EXPORT_OK = qw(%mltable);

use strict;

use vars qw($VERSION %mltable);

$VERSION = 99.1117;

CONFIG:	{
	%mltable = qw(
		 1	31
		 3	31
		 4	30
		 5	31
		 6	30
		 7	31
		 8	31
		 9	30
		10	31
		11	30
		12	31);
}

sub days_in
{
	# Month is 1..12
	my ($year, $month) = @_;
	return $mltable{$month+0} unless $month == 2;
	return 28 unless &is_leap($year);
	return 29;
}

sub is_leap
{
	my ($year) = @_;
	return 0 unless $year % 4 == 0;
	return 1 unless $year % 100 == 0;
	return 0 unless $year % 400 == 0;
	return 1;
}

1;

__DATA__

=head1 NAME

Time::DaysInMonth -- simply report the number of days in a month

=head1 SYNOPSIS

	use Time::DaysInMonth;
	$days = days_in($year, $month_1_to_12);
	$leapyear = is_leap($year);

=head1 DESCRIPTION

DaysInMonth is simply a package to report the number of days in
a month.  That's all it does.  Really!

=head1 AUTHOR

David Muir Sharnoff <muir@idiom.com>

=head1 LICENSE

Copyright (C) 1996-1999 David Muir Sharnoff.  License hereby
granted for anyone to use, modify or redistribute this module at
their own risk.  Please feed useful changes back to muir@idiom.com.

