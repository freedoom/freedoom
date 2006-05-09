package Time::JulianDay;

require 5.000;

use Carp;
use Time::Timezone;

@ISA = qw(Exporter);
@EXPORT = qw(julian_day inverse_julian_day day_of_week 
	jd_secondsgm jd_secondslocal 
	jd_timegm jd_timelocal 
	gm_julian_day local_julian_day 
	);
@EXPORT_OK = qw($brit_jd);

use strict;
use integer;

# constants
use vars qw($brit_jd $jd_epoch $jd_epoch_remainder $VERSION);

$VERSION = 99.061501;

# calculate the julian day, given $year, $month and $day
sub julian_day
{
    my($year, $month, $day) = @_;
    my($tmp);

    use Carp;
#    confess() unless defined $day;

    $tmp = $day - 32075
      + 1461 * ( $year + 4800 - ( 14 - $month ) / 12 )/4
      + 367 * ( $month - 2 + ( ( 14 - $month ) / 12 ) * 12 ) / 12
      - 3 * ( ( $year + 4900 - ( 14 - $month ) / 12 ) / 100 ) / 4
      ;

    return($tmp);

}

sub gm_julian_day
{
    my($secs) = @_;
    my($sec, $min, $hour, $mon, $year, $day, $month);
    ($sec, $min, $hour, $day, $mon, $year) = gmtime($secs);
    $month = $mon + 1;
    $year += 1900;
    return julian_day($year, $month, $day)
}

sub local_julian_day
{
    my($secs) = @_;
    my($sec, $min, $hour, $mon, $year, $day, $month);
    ($sec, $min, $hour, $day, $mon, $year) = localtime($secs);
    $month = $mon + 1;
    $year += 1900;
    return julian_day($year, $month, $day)
}

sub day_of_week
{
	my ($jd) = @_;
        return (($jd + 1) % 7);       # calculate weekday (0=Sun,6=Sat)
}


# The following defines the first day that the Gregorian calendar was used
# in the British Empire (Sep 14, 1752).  The previous day was Sep 2, 1752
# by the Julian Calendar.  The year began at March 25th before this date.

$brit_jd = 2361222;

# Usage:  ($year,$month,$day) = &inverse_julian_day($julian_day)
sub inverse_julian_day
{
        my($jd) = @_;
        my($jdate_tmp);
        my($m,$d,$y);

        carp("warning: julian date $jd pre-dates British use of Gregorian calendar\n")
                if ($jd < $brit_jd);

        $jdate_tmp = $jd - 1721119;
        $y = (4 * $jdate_tmp - 1)/146097;
        $jdate_tmp = 4 * $jdate_tmp - 1 - 146097 * $y;
        $d = $jdate_tmp/4;
        $jdate_tmp = (4 * $d + 3)/1461;
        $d = 4 * $d + 3 - 1461 * $jdate_tmp;
        $d = ($d + 4)/4;
        $m = (5 * $d - 3)/153;
        $d = 5 * $d - 3 - 153 * $m;
        $d = ($d + 5) / 5;
        $y = 100 * $y + $jdate_tmp;
        if($m < 10) {
                $m += 3;
        } else {
                $m -= 9;
                ++$y;
        }
        return ($y, $m, $d);
}

{
	my($sec, $min, $hour, $day, $mon, $year) = gmtime(0);
	$year += 1900;
	if ($year == 1970 && $mon == 0 && $day == 1) {
		# standard unix time format
		$jd_epoch = 2440588;
	} else {
		$jd_epoch = julian_day($year, $mon+1, $day);
	}
	$jd_epoch_remainder = $hour*3600 + $min*60 + $sec;
}

sub jd_secondsgm
{
	my($jd, $hr, $min, $sec) = @_;

	my($r) =  (($jd - $jd_epoch) * 86400 
		+ $hr * 3600 + $min * 60 
		- $jd_epoch_remainder);

	no integer;
	return ($r + $sec);
	use integer;
}

sub jd_secondslocal
{
	my($jd, $hr, $min, $sec) = @_;
	my $jds = jd_secondsgm($jd, $hr, $min, $sec);
	return $jds - tz_local_offset($jds);
}

# this uses a 0-11 month to correctly reverse localtime()
sub jd_timelocal
{
	my ($sec,$min,$hours,$mday,$mon,$year) = @_;
	$year += 1900 unless $year > 1000;
	my $jd = julian_day($year, $mon+1, $mday);
	my $jds = jd_secondsgm($jd, $hours, $min, $sec);
	return $jds - tz_local_offset($jds);
}

# this uses a 0-11 month to correctly reverse gmtime()
sub jd_timegm
{
	my ($sec,$min,$hours,$mday,$mon,$year) = @_;
	$year += 1900 unless $year > 1000;
	my $jd = julian_day($year, $mon+1, $mday);
	return jd_secondsgm($jd, $hours, $min, $sec);
}

1;

__DATA__

=head1 NAME

Time::JulianDay -- Julian calendar manipulations

=head1 SYNOPSIS

	use Time::JulianDay

	$jd = julian_day($year, $month_1_to_12, $day)
	$jd = local_julian_day($seconds_since_1970);
	$jd = gm_julian_day($seconds_since_1970);
	($year, $month_1_to_12, $day) = inverse_julian_day($jd)
	$dow = day_of_week($jd) 

	print (Sun,Mon,Tue,Wed,Thu,Fri,Sat)[$dow];

	$seconds_since_jan_1_1970 = jd_secondslocal($jd, $hour, $min, $sec)
	$seconds_since_jan_1_1970 = jd_secondsgm($jd, $hour, $min, $sec)
	$seconds_since_jan_1_1970 = jd_timelocal($sec,$min,$hours,$mday,$month_0_to_11,$year)
	$seconds_since_jan_1_1970 = jd_timegm($sec,$min,$hours,$mday,$month_0_to_11,$year)

=head1 DESCRIPTION

JulianDay is a package that manipulates dates as number of days since 
some time a long time ago.  It's easy to add and subtract time
using julian days...  

The day_of_week returned by day_of_week() is 0 for Sunday, and 6 for
Saturday and everything else is in between.

=head1 GENESIS

Written by David Muir Sharnoff <muir@idiom.com> with help from
previous work by 
Kurt Jaeger aka PI <zrzr0111@helpdesk.rus.uni-stuttgart.de>
 	based on postings from: Ian Miller <ian_m@cix.compulink.co.uk>;
Gary Puckering <garyp%cognos.uucp@uunet.uu.net>
	based on Collected Algorithms of the ACM ?;
and the unknown-to-me author of Time::Local.

=head1 LICENSE

Copyright (C) 1996-1999 David Muir Sharnoff.  License hereby
granted for anyone to use, modify or redistribute this module at
their own risk.  Please feed useful changes back to muir@idiom.com.

