package Time::CTime;


require 5.000;

use Time::Timezone;
use Time::CTime;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(ctime asctime strftime);
@EXPORT_OK = qw(asctime_n ctime_n @DoW @MoY @DayOfWeek @MonthOfYear);

use strict;

# constants
use vars qw(@DoW @DayOfWeek @MoY @MonthOfYear %strftime_conversion $VERSION);
use vars qw($template $sec $min $hour $mday $mon $year $wday $yday $isdst);

$VERSION = 99.06_22_01;

CONFIG: {
    @DoW = 	   qw(Sun Mon Tue Wed Thu Fri Sat);
    @DayOfWeek =   qw(Sunday Monday Tuesday Wednesday Thursday Friday Saturday);
    @MoY = 	   qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
    @MonthOfYear = qw(January February March April May June 
		      July August September October November December);
  
    %strftime_conversion = (
	'%',	sub { '%' },
	'a',	sub { $DoW[$wday] },
	'A',	sub { $DayOfWeek[$wday] },
	'b',	sub { $MoY[$mon] },
	'B',	sub { $MonthOfYear[$mon] },
	'c',	sub { asctime_n($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst, "") },
	'd',	sub { sprintf("%02d", $mday); },
	'D',	sub { sprintf("%02d/%02d/%02d", $mon+1, $mday, $year%100) },
	'e',	sub { sprintf("%2d", $mday); },
	'f',	sub { fracprintf ("%3.3f", $sec); },
	'F',	sub { fracprintf ("%6.6f", $sec); },
	'h',	sub { $MoY[$mon] },
	'H',	sub { sprintf("%02d", $hour) },
	'I',	sub { sprintf("%02d", $hour % 12 || 12) },
	'j',	sub { sprintf("%03d", $yday + 1) },
	'k',	sub { sprintf("%2d", $hour); },
	'l',	sub { sprintf("%2d", $hour % 12 || 12) },
	'm',	sub { sprintf("%02d", $mon+1); },
	'M',	sub { sprintf("%02d", $min) },
	'n',	sub { "\n" },
	'o',	sub { sprintf("%d%s", $mday, (($mday < 20 && $mday > 3) ? 'th' : ($mday%10 == 1 ? "st" : ($mday%10 == 2 ? "nd" : ($mday%10 == 3 ? "rd" : "th"))))) },
	'p',	sub { $hour > 11 ? "PM" : "AM" },
	'r',	sub { sprintf("%02d:%02d:%02d %s", $hour % 12 || 12, $min, $sec, $hour > 11 ? 'PM' : 'AM') },
	'R',	sub { sprintf("%02d:%02d", $hour, $min) },
	'S',	sub { sprintf("%02d", $sec) },
	't',	sub { "\t" },
	'T',	sub { sprintf("%02d:%02d:%02d", $hour, $min, $sec) },
	'U',	sub { wkyr(0, $wday, $yday) },
	'w',	sub { $wday },
	'W',	sub { wkyr(1, $wday, $yday) },
	'y',	sub { sprintf("%02d",$year%100) },
	'Y',	sub { $year + 1900 },
	'x',	sub { sprintf("%02d/%02d/%02d", $mon + 1, $mday, $year%100) },
	'X',	sub { sprintf("%02d:%02d:%02d", $hour, $min, $sec) },
	'Z',	sub { &tz2zone(undef,undef,$isdst) }
    );


}

sub fracprintf {
    my($t,$s) = @_;
    my($p) = sprintf($t, $s-int($s));
    $p=~s/^0+//;
    $p;
}

sub asctime_n {
    my($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst, $TZname) = @_;
    ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst, $TZname) = localtime($sec) unless defined $min;
    $year += 1900;
    $TZname .= ' ' 
	if $TZname;
    sprintf("%s %s %2d %2d:%02d:%02d %s%4d",
	  $DoW[$wday], $MoY[$mon], $mday, $hour, $min, $sec, $TZname, $year);
}

sub asctime
{
    return asctime_n(@_)."\n";
}

# is this formula right?
sub wkyr {
    my($wstart, $wday, $yday) = @_;
    $wday = ($wday + 7 - $wstart) % 7;
    return int(($yday - $wday + 13) / 7 - 1);
}

# ctime($time)

sub ctime {
    my($time) = @_;
    asctime(localtime($time), &tz2zone(undef,$time));
}

sub ctime_n {
    my($time) = @_;
    asctime_n(localtime($time), &tz2zone(undef,$time));
}

# strftime($template, @time_struct)
#
# Does not support locales

sub strftime {			
    local ($template, $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = @_;

    undef $@;
    $template =~ s/%([%aAbBcdDefFhHIjklmMnopQrRStTUwWxXyYZ])/&{$Time::CTime::strftime_conversion{$1}}()/egs;
    die $@ if $@;
    return $template;
}

1;

__DATA__

=head1 NAME

Time::CTime -- format times ala POSIX asctime

=head1 SYNOPSIS

	use Time::CTime
 	print ctime(time);
	print asctime(localtime(time));
	print strftime(template, localtime(time)); 

=head2 strftime conversions

	%%	PERCENT
	%a	day of the week abbr
	%A	day of the week
	%b	month abbr
	%B 	month
	%c 	ctime format: Sat Nov 19 21:05:57 1994
	%d 	DD
	%D 	MM/DD/YY
	%e 	numeric day of the month
	%f 	floating point seconds (milliseconds): .314
	%F 	floating point seconds (microseconds): .314159
	%h 	month abbr
	%H 	hour, 24 hour clock, leading 0's)
	%I 	hour, 12 hour clock, leading 0's)
	%j 	day of the year
	%k 	hour
	%l 	hour, 12 hour clock
	%m 	month number, starting with 1
	%M 	minute, leading 0's
	%n 	NEWLINE
	%o	ornate day of month -- "1st", "2nd", "25th", etc.
	%p 	AM or PM 
	%r 	time format: 09:05:57 PM
	%R 	time format: 21:05
	%S 	seconds, leading 0's
	%t 	TAB
	%T 	time format: 21:05:57
	%U 	week number, Sunday as first day of week
	%w 	day of the week, numerically, Sunday == 0
	%W 	week number, Monday as first day of week
	%x 	date format: 11/19/94
	%X 	time format: 21:05:57
	%y	year (2 digits)
	%Y	year (4 digits)
	%Z 	timezone in ascii. eg: PST

=head1 DESCRIPTION

This module provides routines to format dates.  They correspond 
to the libc routines.  &strftime() supports a pretty good set of
coversions -- more than most C libraries.
 
strftime supports a pretty good set of conversions.  

The POSIX module has very similar functionality.  You should consider
using it instead if you do not have allergic reactions to system 
libraries.

=head1 GENESIS

Written by David Muir Sharnoff <muir@idiom.com>.

The starting point for this package was a posting by 
Paul Foley <paul@ascent.com> 

=head1 LICENSE

Copyright (C) 1996-1999 David Muir Sharnoff.  License hereby
granted for anyone to use, modify or redistribute this module at
their own risk.  Please feed useful changes back to muir@idiom.com.

