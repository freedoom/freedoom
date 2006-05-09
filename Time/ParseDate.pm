
package Time::ParseDate;

require 5.000;

use Carp;
use Time::Timezone;
use Time::JulianDay;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(parsedate);
@EXPORT_OK = qw(pd_raw %mtable %umult %wdays);

use strict;

# constants
use vars qw(%mtable %umult %wdays $VERSION);

$VERSION = 2003.0211;

# globals
use vars qw($debug); 

# dynamically-scoped
use vars qw($parse);

my %mtable;
my %umult;
my %wdays;
my $y2k;

CONFIG:	{

	%mtable = qw(
		Jan 1	Jan. 1	January 1
		Feb 2	Feb. 2	February 2
		Mar 3	Mar. 3	March 3
		Apr 4	Apr. 4	April 4
		May 5 
		Jun 6	Jun. 6	June 6 
		Jul 7	Jul. 7	July 7 
		Aug 8	Aug. 8	August 8 
		Sep 9	Sep. 9	September 9 
		Oct 10	Oct. 10	October 10 
		Nov 11	Nov. 11	November 11 
		Dec 12	Dec. 12	December 12 );
	%umult = qw(
		sec 1 second 1
		min 60 minute 60
		hour 3600
		day 86400
		week 604800 );
	%wdays = qw(
		sun 0 sunday 0
		mon 1 monday 1
		tue 2 tuesday 2
		wed 3 wednesday 3
		thu 4 thursday 4
		fri 5 friday 5
		sat 6 saturday 6
		);

	$y2k = 946684800; # turn of the century
}

sub parsedate
{
	my ($t, %options) = @_;

	my ($y, $m, $d);	# year, month - 1..12, day
	my ($H, $M, $S);	# hour, minute, second
	my $tz;		 	# timezone
	my $tzo;		# timezone offset
	my ($rd, $rs);		# relative days, relative seconds

	my $rel; 		# time&|date is relative

	my $isspec;
	my $now = $options{NOW} || time;
	my $passes = 0;
	my $uk = defined($options{UK}) ? $options{UK} : 0;

	local $parse = '';  # will be dynamically scoped.

	if ($t =~ s#^   ([ \d]\d) 
			/ (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
			/ (\d\d\d\d)
			: (\d\d)
			: (\d\d)
			: (\d\d)
			(?:
			 [ ]
			 ([-+] \d\d\d\d)
			  (?: \("?(?:(?:[A-Z]{1,4}[TCW56])|IDLE)\))?
			 )?
			##xi) { #"emacs
		# [ \d]/Mon/yyyy:hh:mm:ss [-+]\d\d\d\d
		# This is the format for www server logging.

		($d, $m, $y, $H, $M, $S, $tzo) = ($1, $mtable{"\u\L$2"}, $3, $4, $5, $6, $7 ? &mkoff($7) : ($tzo || undef));
		$parse .= " ".__LINE__ if $debug;
	} elsif ($t =~ s#^(\d\d)/(\d\d)/(\d\d)\.(\d\d)\:(\d\d)(\s+|$)##) {
		# yy/mm/dd.hh:mm
		# I support this format because it's used by wbak/rbak
		# on Apollo Domain OS.  Silly, but historical.

		($y, $m, $d, $H, $M, $S) = ($1, $2, $3, $4, $5, 0);
		$parse .= " ".__LINE__ if $debug;
	} else {
		while(1) {
			if (! defined $m and ! defined $rd and ! defined $y
				and ! ($passes == 0 and $options{'TIMEFIRST'}))
			{
				# no month defined.
				if (&parse_date_only(\$t, \$y, \$m, \$d, $uk)) {
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			if (! defined $H and ! defined $rs) {
				if (&parse_time_only(\$t, \$H, \$M, \$S, 
					\$tz, %options)) 
				{
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			next if $passes == 0 and $options{'TIMEFIRST'};
			if (! defined $y) {
				if (&parse_year_only(\$t, \$y, $now, %options)) {
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			if (! defined $tz and ! defined $tzo and ! defined $rs 
				and (defined $m or defined $H)) 
			{
				if (&parse_tz_only(\$t, \$tz, \$tzo)) {
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			if (! defined $H and ! defined $rs) {
				if (&parse_time_offset(\$t, \$rs, %options)) {
					$rel = 1;
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			if (! defined $m and ! defined $rd and ! defined $y) {
				if (&parse_date_offset(\$t, $now, \$y, 
					\$m, \$d, \$rd, \$rs, %options)) 
				{
					$rel = 1;
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			if (defined $M or defined $rd) {
				if ($t =~ s/^\s*(?:at|\+)\s*(\s+|$)//x) {
					$rel = 1;
					$parse .= " ".__LINE__ if $debug;
					next;
				}
			}
			last;
		} continue {
			$passes++;
			&debug_display($tz, $tzo, $H, $M, $S, $m, $d, $y, $rs, $rd, $rel, $passes, $parse, $t) if $debug;

		}

		if ($passes == 0) {
			print "nothing matched\n" if $debug;
			return (undef, "no match on time/date") 
				if wantarray();
			return undef;
		}
	}

	&debug_display($tz, $tzo, $H, $M, $S, $m, $d, $y, $rs, $rd, $rel, $passes, $parse, $t) if $debug;

	$t =~ s/^\s+//;

	if ($t ne '') {
		# we didn't manage to eat the string
		print "NOT WHOLE\n" if $debug;
		if ($options{WHOLE}) {
			return (undef, "characters left over after parse")
				if wantarray();
			return undef 
		}
	}

	# define a date if there isn't one already

	if (! defined $y and ! defined $m and ! defined $rd) {
		print "no date defined, trying to find one." if $debug;
		if (defined $rs or defined $H) {
			# we do have a time.
			if ($options{DATE_REQUIRED}) {
				return (undef, "no date specified")
					if wantarray();
				return undef;
			}
			if (defined $rs) {
				print "simple offset: $rs\n" if $debug;
				my $rv = $now + $rs;
				return ($rv, $t) if wantarray();
				return $rv;
			}
			$rd = 0;
		} else {
			print "no time either!\n" if $debug;
			return (undef, "no time specified")
				if wantarray();
			return undef;
		}
	}

	if ($options{TIME_REQUIRED} && ! defined($rs) 
		&& ! defined($H) && ! defined($rd))
	{
		return (undef, "no time found")
			if wantarray();
		return undef;
	}

	my $secs;
	my $jd;

	if (defined $rd) {
		if (defined $rs || ! (defined($H) || defined($M) || defined($S))) {
			print "fully relative\n" if $debug;
			my ($j, $in, $it);
			my $definedrs = defined($rs) ? $rs : 0;
			my ($isdst_now, $isdst_then);
			my $r = $now + $rd * 86400 + $definedrs;
			#
			# It's possible that there was a timezone shift 
			# during the time specified.  If so, keep the
			# hours the "same".
			#
			$isdst_now = (localtime($r))[8];
			$isdst_then = (localtime($now))[8];
			if (($isdst_now == $isdst_then) || $options{GMT})
			{
				return ($r, $t) if wantarray();
				return $r 
			}
				
			print "localtime changed DST during time period!\n" if $debug;
		}

		print "relative date\n" if $debug;
		$jd = local_julian_day($now);
		print "jd($now) = $jd\n" if $debug;
		$jd += $rd;
	} else {
		unless (defined $y) {
			if ($options{PREFER_PAST}) {
				my ($day, $mon011);
				($day, $mon011, $y) = (&righttime($now))[3,4,5];

				print "calc year -past $day-$d $mon011-$m $y\n" if $debug;
				$y -= 1 if ($mon011+1 < $m) || 
					(($mon011+1 == $m) && ($day < $d));
			} elsif ($options{PREFER_FUTURE}) {
				print "calc year -future\n" if $debug;
				my ($day, $mon011);
				($day, $mon011, $y) = (&righttime($now))[3,4,5];
				$y += 1 if ($mon011 >= $m) || 
					(($mon011+1 == $m) && ($day > $d));
			} else {
				print "calc year -this\n" if $debug;
				$y = (localtime($now))[5];
			}
			$y += 1900;
		}

		$y = expand_two_digit_year($y, $now, %options)
			if $y < 100;

		if ($options{VALIDATE}) {
			require Time::DaysInMonth;
			my $dim = Time::DaysInMonth::days_in($y, $m);
			if ($y < 1000 or $m < 1 or $d < 1 
				or $y > 9999 or $m > 12 or $d > $dim)
			{
				return (undef, "illegal YMD: $y, $m, $d")
					if wantarray();
				return undef;
			}
		}
		$jd = julian_day($y, $m, $d);
		print "jd($y, $m, $d) = $jd\n" if $debug;
	}

	# put time into HMS

	if (! defined($H)) {
		if (defined($rd) || defined($rs)) {
			($S, $M, $H) = &righttime($now, %options);
			print "HMS set to $H $M $S\n" if $debug;
		} 
	}

	my $carry;

	print "before ", (defined($rs) ? "$rs" : ""),
		    " $jd $H $M $S\n" 
		if $debug;
	#
	# add in relative seconds.  Do it this way because we want to
	# preserve the localtime across DST changes.
	#

	$S = 0 unless $S; # -w
	$M = 0 unless $M; # -w
	$H = 0 unless $H; # -w

	if ($options{VALIDATE} and
		($S < 0 or $M < 0 or $H < 0 or $S > 59 or $M > 59 or $H > 23)) 
	{
		return (undef, "illegal HMS: $H, $M, $S") if wantarray();
		return undef;
	}

	$S += $rs if defined $rs;
	$carry = int($S / 60);
	my($frac) = $S - int($S);
	$S = int($S);
	$S %= 60;
	$S += $frac;
	$M += $carry;
	$carry = int($M / 60);
	$M %= 60;
	$H += $carry;
	$carry = int($H / 24);
	$H %= 24;
	$jd += $carry;

	print "after rs  $jd $H $M $S\n" if $debug;

	$secs = jd_secondsgm($jd, $H, $M, $S);
	print "jd_secondsgm($jd, $H, $M, $S) = $secs\n" if $debug;

	# 
	# If we see something link 3pm CST then and we want to end
	# up with a GMT seconds, then we convert the 3pm to GMT and
	# subtract in the offset for CST.  We subtract because we
	# are converting from CST to GMT.
	#
	my $tzadj;
	if ($tz) {
		$tzadj = tz_offset($tz, $secs);
		print "adjusting secs for $tz: $tzadj\n" if $debug;
		$tzadj = tz_offset($tz, $secs-$tzadj);
		$secs -= $tzadj;
	} elsif (defined $tzo) {
		print "adjusting time for offset: $tzo\n" if $debug;
		$secs -= $tzo;
	} else {
		unless ($options{GMT}) {
			if ($options{ZONE}) {
				$tzadj = tz_offset($options{ZONE}, $secs);
				$tzadj = tz_offset($options{ZONE}, $secs-$tzadj);
				print "adjusting secs for $options{ZONE}: $tzadj\n" if $debug;
				$secs -= $tzadj;
			} else {
				$tzadj = tz_local_offset($secs);
				print "adjusting secs for local offset: $tzadj\n" if $debug;
				# 
				# Just in case we are very close to a time
				# change...
				#
				$tzadj = tz_local_offset($secs-$tzadj);
				$secs -= $tzadj;
			}
		}
	}

	print "returning $secs.\n" if $debug;

	return ($secs, $t) if wantarray();
	return $secs;
}


sub mkoff
{
	my($offset) = @_;

	if (defined $offset and $offset =~ s#^([-+])(\d\d)(\d\d)$##) {
		return ($1 eq '+' ? 
			  3600 * $2  + 60 * $3
			: -3600 * $2 + -60 * $3 );
	}
	return undef;
}

sub parse_tz_only
{
	my($tr, $tz, $tzo) = @_;

	$$tr =~ s#^\s+##;
	my $o;

	if ($$tr =~ s#^
			([-+]\d\d\d\d)
			\s+
			\(
				"?
				(?:
					(?:
						[A-Z]{1,4}[TCW56]
					)
					|
					IDLE
				)
			\)
			(?:
				\s+
				|
				$ 
			)
			##x) { #"emacs
		$$tzo = &mkoff($1);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^GMT\s*([-+]\d{1,2})(\s+|$)##x) {
		$o = $1;
		if ($o <= 24 and $o !~ /^0/) {
			# probably hours.
			printf "adjusted at %d. ($o 00)\n", __LINE__ if $debug;
			$o = "${o}00";
		}
		$o =~ s/\b(\d\d\d)/0$1/;
		$$tzo = &mkoff($o);
		printf "matched at %d. ($$tzo, $o)\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?:GMT\s*)?([-+]\d\d\d\d)(\s+|$)##x) {
		$o = $1;
		$$tzo = &mkoff($o);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^"?((?:[A-Z]{1,4}[TCW56])|IDLE)(?:\s+|$ )##x) { #"
		$$tz = $1;
		$$tz .= " DST" 
			if $$tz eq 'MET' && $$tr =~ s#^DST(?:\s+|$ )##x;
		printf "matched at %d: '$$tz'.\n", __LINE__ if $debug;
		return 1;
	}
	return 0;
}

sub parse_date_only
{
	my ($tr, $yr, $mr, $dr, $uk) = @_;

	$$tr =~ s#^\s+##;

	if ($$tr =~ s#^(\d\d\d\d)([-./])(\d\d?)\2(\d\d?)(\s+|$)##) {
		# yyyy/mm/dd

		($$yr, $$mr, $$dr) = ($1, $3, $4);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(\d\d?)([-./])(\d\d?)\2(\d\d\d\d?)(\s+|$)##) {
		# mm/dd/yyyy - is this safe?  No.
		# -- or dd/mm/yyyy! If $1>12, then it's umabiguous.
		# Otherwise check option UK for UK style date.
		if ($uk || $1>12) {
		  ($$yr, $$mr, $$dr) = ($4, $3, $1);
		} else {
		  ($$yr, $$mr, $$dr) = ($4, $1, $3);
		}
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(\d\d\d\d)/(\d\d?)(?:\s|$ )##x) {
		# yyyy/mm

		($$yr, $$mr, $$dr) = ($1, $2, 1);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(?:
				(?:Mon|Monday|Tue|Tuesday|Wed|Wednesday|
					Thu|Thursday|Fri|Friday|
					Sat|Saturday|Sun|Sunday),?
				\s+
			)?
			(\d\d?)
			(\s+ | - | \. | /)
			(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?
			(?:
				\2
				(\d\d (?:\d\d)? )
			)?
			(?:
				\s+
			|
				$
			)
			##) {
		# [Dow,] dd Mon [yy[yy]]
		($$yr, $$mr, $$dr) = ($4, $mtable{"\u\L$3"}, $1);

		printf "%d: %s - %s - %s\n", __LINE__, $1, $2, $3 if $debug;
		print "y undef\n" if ($debug && ! defined($$yr));
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(?:
				(?:Mon|Monday|Tue|Tuesday|Wed|Wednesday|
					Thu|Thursday|Fri|Friday|
					Sat|Saturday|Sun|Sunday),?
				\s+
			)?
			(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?
			((\s)+ | - | \. | /)
				
			(\d\d?)
			(?:
				(?: \2|\3+)
				(\d\d (?: \d\d)?)
			)?
			(?:
				\s+
			|
				$
			)
			##) {
		# [Dow,] Mon dd [yyyy]
		($$yr, $$mr, $$dr) = ($5, $mtable{"\u\L$1"}, $4);
		printf "%d: %s - %s - %s\n", __LINE__, $1, $2, $4 if $debug;
		print "y undef\n" if ($debug && ! defined($$yr));
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(January|Jan\.?|February|Feb\.?|March|Mar\.?|April|Apr\.?|May|
			    June|Jun\.?|July|Jul\.?|August|Aug\.?|September|Sep\.?|
			    October|Oct\.?|November|Nov\.?|December|Dec\.?)
			\s+
			(\d+)
			(?:st|nd|rd|th)?
			\,?
			(?: 
				\s+
				(?:
					(\d\d\d\d)
					|(?:\' (\d\d))
				)
			)?
			(?:
				\s+
			|
				$
			)
			##) {
		# Month day{st,nd,rd,th}, 'yy
		# Month day{st,nd,rd,th}, year
		($$yr, $$mr, $$dr) = ($3 || $4, $mtable{"\u\L$1"}, $2);
		printf "%d: %s - %s - %s - %s\n", __LINE__, $1, $2, $3, $4 if $debug;
		print "y undef\n" if ($debug && ! defined($$yr));
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(\d\d?)([-/.])(\d\d?)\2(\d\d?)(\s+|$)##x) {
		if ($1 > 31 || (!$uk && $1 > 12 && $4 < 32)) {
			# yy/mm/dd
			($$yr, $$mr, $$dr) = ($1, $3, $4);
		} elsif ($1 > 12 || $uk) {
			# dd/mm/yy
			($$yr, $$mr, $$dr) = ($4, $3, $1);
		} else {
			# mm/dd/yy
			($$yr, $$mr, $$dr) = ($4, $1, $3);
		}
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(\d\d?)/(\d\d?)(\s+|$)##x) {
		if ($1 > 31 || (!$uk && $1 > 12)) {
			# yy/mm
			($$yr, $$mr, $$dr) = ($1, $2, 1);
		} elsif ($2 > 31 || ($uk && $2 > 12)) {
			# mm/yy
			($$yr, $$mr, $$dr) = ($2, $1, 1);
		} elsif ($1 > 12 || $uk) {
			# dd/mm
			($$mr, $$dr) = ($2, $1);
		} else {
			# mm/dd
			($$mr, $$dr) = ($1, $2);
		}
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(\d\d)(\d\d)(\d\d)(\s+|$)##x) {
		if ($1 > 31 || (!$uk && $1 > 12)) {
			# YYMMDD
			($$yr, $$mr, $$dr) = ($1, $2, $3);
		} elsif ($1 > 12 || $uk) {
			# DDMMYY
			($$yr, $$mr, $$dr) = ($3, $2, $1);
		} else {
			# MMDDYY
			($$yr, $$mr, $$dr) = ($3, $1, $2);
		}
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(\d{1,2})
			(\s+ | - | \. | /)
			(January|Jan\.?|February|Feb\.?|March|Mar\.?|April|Apr\.?|May|
			    June|Jun\.?|July|Jul\.?|August|Aug\.?|September|Sep\.?|
			    October|Oct\.?|November|Nov\.?|December|Dec\.?)
			(?:
				\2
				(
					\d\d
					(?:\d\d)?
				)
			)
			(:?
				\s+
			|
				$
			)
			##) {
		# dd Month [yr]
		($$yr, $$mr, $$dr) = ($4, $mtable{"\u\L$3"}, $1);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(\d+)
			(?:st|nd|rd|th)?
			\s+
			(January|Jan\.?|February|Feb\.?|March|Mar\.?|April|Apr\.?|May|
			    June|Jun\.?|July|Jul\.?|August|Aug\.?|September|Sep\.?|
			    October|Oct\.?|November|Nov\.?|December|Dec\.?)
			(?: 
				\,?
				\s+
				(\d\d\d\d)
			)?
			(:?
				\s+
			|
				$
			)
			##) {
		# day{st,nd,rd,th}, Month year
		($$yr, $$mr, $$dr) = ($3, $mtable{"\u\L$2"}, $1);
		printf "%d: %s - %s - %s - %s\n", __LINE__, $1, $2, $3, $4 if $debug;
		print "y undef\n" if ($debug && ! defined($$yr));
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	}
	return 0;
}

sub parse_time_only
{
	my ($tr, $hr, $mr, $sr, $tzr, %options) = @_;

	$$tr =~ s#^\s+##;

	if ($$tr =~ s!^(?x)
			(?:
				(?:
					([012]\d)		(?# $1)
					(?:
						([0-5]\d) 	(?# $2)
						(?:
						    ([0-5]\d)	(?# $3)
						)?
					)
					\s*
					([ap]m)?  		(?# $4)
				) | (?:
					(\d{1,2}) 		(?# $5)
					(?:
						\:
						(\d\d)		(?# $6)
						(?:
							\:
							(\d\d)	(?# $7)
								(
									(?# don't barf on database sub-second timings)
									(?:\:|\.)
									\d{1,6}
								)?	(?# $8)
						)?
					)
					\s*
					([apAP][mM])?		(?# $9)
				) | (?:
					(\d{1,2})		(?# $10)
					([apAP][mM])		(?# ${11})
				)
			)
			(?:
				\s+
				"?
				(				(?# ${12})
					(?: [A-Z]{1,4}[TCW56] )
					|
					IDLE
				)	
			)?
			(?:
				\s*
			|
				$
			)
			!!) { #"emacs
		# HH[[:]MM[:SS]]meridan [zone] 
		my $ampm;
		$$hr = $1 || $5 || $10 || 0; # 10 is undef, but 5 is defined..
		$$mr = $2 || $6 || 0;
		$$sr = $3 || $7 || 0;
		if (defined($8) && exists($options{SUBSECOND}) && $options{SUBSECOND}) {
			my($frac) = $8;
			substr($frac,0,1) = '.';
			$$sr += $frac;
		}
		print "S = $$sr\n" if $debug;
		$ampm = $4 || $9 || $11;
		$$tzr = $12;
		$$hr += 12 if $ampm and "\U$ampm" eq "PM" && $$hr != 12;
		$$hr = 0 if $$hr == 12 && "\U$ampm" eq "AM";
		$$hr = 0 if $$hr == 24;
		printf "matched at %d, rem = %s.\n", __LINE__, $$tr if $debug;
		return 1;
	} elsif ($$tr =~ s#noon(?:\s+|$ )##ix) {
		# noon
		($$hr, $$mr, $$sr) = (12, 0, 0);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#midnight(?:\s+|$ )##ix) {
		# midnight
		($$hr, $$mr, $$sr) = (0, 0, 0);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	}
	return 0;
}

sub parse_time_offset
{
	my ($tr, $rsr, %options) = @_;

	$$tr =~ s/^\s+//;

	return 0 if $options{NO_RELATIVE};

	if ($$tr =~ s#^(?xi)
			([-+]?)
			\s*
			(\d+)
			\s*
			(sec|second|min|minute|hour)s?
			(
				\s+
				ago
			)?
			(?:
				\s+
				|
				$
			)
			##) {
		# count units
		$$rsr = 0 unless defined $$rsr;
		$$rsr += $umult{"\L$3"} * "$1$2";

		$$rsr = -$$rsr if $4 ||
			$$tr =~ /\b(day|mon|month|year)s?\s*ago\b/;
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} 
	return 0;
}

#
# What to you do with a date that has a two-digit year?
# There's not much that can be done except make a guess.
#
# Some example situations to handle:
#
#	now		year 
#
#	1999		01
#	1999		71
#	2010		71
#	2110		09
#

sub expand_two_digit_year
{
	my ($yr, $now, %options) = @_;

	return $yr if $yr > 100;

	my ($y) = (&righttime($now, %options))[5];
	$y += 1900;
	my $century = int($y / 100) * 100;
	my $within = $y % 100;

	my $r = $yr + $century;

	if ($options{PREFER_PAST}) {
		if ($yr > $within) {
			$r = $yr + $century - 100;
		}
	} elsif ($options{PREFER_FUTURE}) {
		# being strict here would be silly
		if ($yr < $within-20) {
			# it's 2019 and the date is '08'
			$r = $yr + $century + 100;
		}
	} elsif ($options{UNAMBIGUOUS}) {
		# we really shouldn't guess
		return undef;
	} else {
		# prefer the current century in most cases

		if ($within > 80 && $within - $yr > 60) {
			$r = $yr + $century + 100;
		}

		if ($within < 30 && $yr - $within > 59) {
			$r = $yr + $century - 100;
		}
	}
	print "two digit year '$yr' expanded into $r\n" if $debug;
	return $r;
}


sub calc 
{
	my ($rsr, $yr, $mr, $dr, $rdr, $now, $units, $count, %options) = @_;

	confess unless $units;
	$units = "\L$units";
	print "calc based on $units\n" if $debug;

	if ($units eq 'day') {
		$$rdr = $count;
	} elsif ($units eq 'week') {
		$$rdr = $count * 7;
	} elsif ($umult{$units}) {
		$$rsr = $count * $umult{$units};
	} elsif ($units eq 'mon' || $units eq 'month') {
		($$yr, $$mr, $$dr) = &monthoff($now, $count, %options);
		$$rsr = 0 unless $$rsr;
	} elsif ($units eq 'year') {
		($$yr, $$mr, $$dr) = &monthoff($now, $count * 12, %options);
		$$rsr = 0 unless $$rsr;
	} else {
		carp "interal error";
	}
	print "calced rsr $$rsr rdr $$rdr, yr $$yr mr $$mr dr $$dr.\n" if $debug;
}

sub monthoff
{
	my ($now, $months, %options) = @_;

	# months are 0..11
	my ($d, $m11, $y) = (&righttime($now, %options)) [ 3,4,5 ] ;

	$y += 1900;

	print "m11 = $m11 + $months, y = $y\n" if $debug;

	$m11 += $months;

	print "m11 = $m11, y = $y\n" if $debug;
	if ($m11 > 11 || $m11 < 0) {
		$y -= 1 if $m11 < 0 && ($m11 % 12 != 0);
		$y += int($m11/12);

		# this is required to work around a bug in perl 5.003
		no integer;
		$m11 %= 12;
	}
	print "m11 = $m11, y = $y\n" if $debug;

	# 
	# What is "1 month from January 31st?"  
	# I think the answer is February 28th most years.
	#
	# Similarly, what is one year from February 29th, 1980?
	# I think it's February 28th, 1981.
	#
	# If you disagree, change the following code.
	#
	if ($d > 30 or ($d > 28 && $m11 == 1)) {
		require Time::DaysInMonth;
		my $dim = Time::DaysInMonth::days_in($y, $m11+1);
		print "dim($y,$m11+1)= $dim\n" if $debug;
		$d = $dim if $d > $dim;
	}
	return ($y, $m11+1, $d);
}

sub righttime
{
	my ($time, %options) = @_;
	if ($options{GMT}) {
		return gmtime($time);
	} else {
		return localtime($time);
	}
}

sub parse_year_only
{
	my ($tr, $yr, $now, %options) = @_;

	$$tr =~ s#^\s+##;

	if ($$tr =~ s#^(\d\d\d\d)(?:\s+|$)##) {
		$$yr = $1;
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#\'(\d\d)(?:\s+|$ )##) {
		$$yr = expand_two_digit_year($1, $now, %options);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	}
	return 0;
}

sub parse_date_offset
{
	my ($tr, $now, $yr, $mr, $dr, $rdr, $rsr, %options) = @_;

	return 0 if $options{NO_RELATIVE};

	# now - current seconds_since_epoch
	# yr - year return
	# mr - month return
	# dr - day return
	# rdr - relatvie day return
	# rsr - relative second return

	my $j;
	my $wday = (&righttime($now, %options))[6];

	$$tr =~ s#^\s+##;

	if ($$tr =~ s#^(?xi)
			\s*
			(\d+)
			\s*
			(day|week|month|year)s?
			(
				\s+
				ago
			)?
			(?:
				\s+
				|
				$
			)
			##) {
		my $amt = $1 + 0;
		my $units = $2;
		$amt = -$amt if $3 ||
			$$tr =~ m#\b(sec|second|min|minute|hour)s?\s*ago\b#;
		&calc($rsr, $yr, $mr, $dr, $rdr, $now, $units, 
			$amt, %options);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(?:
				(?:
					now
					\s+
				)?
				(\+ | \-)
				\s*
			)?
			(\d+)
			\s*
			(day|week|month|year)s?
			(?:
				\s+
				|
				$
			)
			##) {
		my $one = $1 || '';
		my $two = $2 || '';
		my $amt = "$one$two"+0;
		&calc($rsr, $yr, $mr, $dr, $rdr, $now, $3, 
			$amt, %options);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday
				|Wednesday|Thursday|Friday|Saturday|Sunday)
			\s+
			after
			\s+
			next
			(?: \s+ | $ )
			##) {
		# Dow "after next"
		$$rdr = $wdays{"\L$1"} - $wday + ( $wdays{"\L$1"} > $wday ? 7 : 14);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			next\s+
			(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday
				|Wednesday|Thursday|Friday|Saturday|Sunday)
			(?:\s+|$ )
			##) {
		# "next" Dow
		$$rdr = $wdays{"\L$1"} - $wday 
				+ ( $wdays{"\L$1"} > $wday ? 0 : 7);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^(?xi)
			last\s+
			(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday
				|Wednesday|Thursday|Friday|Saturday|Sunday)
			(?:\s+|$ )##) {
		# "last" Dow
		printf "c %d - %d + ( %d < %d ? 0 : -7 \n", $wdays{"\L$1"},  $wday,  $wdays{"\L$1"}, $wday if $debug;
		$$rdr = $wdays{"\L$1"} - $wday + ( $wdays{"\L$1"} < $wday ? 0 : -7);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($options{PREFER_PAST} and $$tr =~ s#^(?xi)
			(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday
				|Wednesday|Thursday|Friday|Saturday|Sunday)
			(?:\s+|$ )##) {
		# Dow
		printf "c %d - %d + ( %d < %d ? 0 : -7 \n", $wdays{"\L$1"},  $wday,  $wdays{"\L$1"}, $wday if $debug;
		$$rdr = $wdays{"\L$1"} - $wday + ( $wdays{"\L$1"} < $wday ? 0 : -7);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($options{PREFER_FUTURE} and $$tr =~ s#^(?xi)
			(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday
				|Wednesday|Thursday|Friday|Saturday|Sunday)
			(?:\s+|$ )
			##) {
		# Dow
		$$rdr = $wdays{"\L$1"} - $wday 
				+ ( $wdays{"\L$1"} > $wday ? 0 : 7);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^today(?:\s+|$ )##xi) {
		# today
		$$rdr = 0;
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^tomorrow(?:\s+|$ )##xi) {
		$$rdr = 1;
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^yesterday(?:\s+|$ )##xi) {
		$$rdr = -1;
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^last\s+(week|month|year)(?:\s+|$ )##xi) {
		&calc($rsr, $yr, $mr, $dr, $rdr, $now, $1, -1, %options);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^next\s+(week|month|year)(?:\s+|$ )##xi) {
		&calc($rsr, $yr, $mr, $dr, $rdr, $now, $1, 1, %options);
		printf "matched at %d.\n", __LINE__ if $debug;
		return 1;
	} elsif ($$tr =~ s#^now (?: \s+ | $ )##x) {
		$$rdr = 0;
		return 1;
	}
	return 0;
}

sub debug_display
{
	my ($tz, $tzo, $H, $M, $S, $m, $d, $y, $rs, $rd, $rel, $passes, $parse, $t) = @_;
	print "---------<<\n";
	print defined($tz) ? "tz: $tz.\n" : "no tz\n";
	print defined($tzo) ? "tzo: $tzo.\n" : "no tzo\n";
	print "HMS: ";
	print defined($H) ? "$H, " : "no H, ";
	print defined($M) ? "$M, " : "no M, ";
	print defined($S) ? "$S\n" : "no S.\n";
	print "mdy: ";
	print defined($m) ? "$m, " : "no m, ";
	print defined($d) ? "$d, " : "no d, ";
	print defined($y) ? "$y\n" : "no y.\n";
	print defined($rs) ? "rs: $rs.\n" : "no rs\n";
	print defined($rd) ? "rd: $rd.\n" : "no rd\n";
	print $rel ? "relative\n" : "not relative\n";
	print "passes: $passes\n";
	print "parse:$parse\n";
	print "t: $t.\n";
	print "--------->>\n";
}
1;

__DATA__

=head1 NAME

Time::ParseDate -- date parsing both relative and absolute

=head1 SYNOPSIS

	use Time::ParseDate;
	$seconds_since_jan1_1970 = parsedate("12/11/94 2pm", NO_RELATIVE => 1)
	$seconds_since_jan1_1970 = parsedate("12/11/94 2pm", %options)

=head1 OPTIONS

Date parsing can also use options.  The options are as follows:

	FUZZY	-> it's okay not to parse the entire date string
	NOW	-> the "current" time for relative times (defaults to time())
	ZONE	-> local timezone (defaults to $ENV{TZ})
	WHOLE	-> the whole input string must be parsed
	GMT	-> input time is assumed to be GMT, not localtime
	UK	-> prefer UK style dates (dd/mm over mm/dd)
	DATE_REQUIRED -> do not default the date
	TIME_REQUIRED -> do not default the time
	NO_RELATIVE -> input time is not relative to NOW
	TIMEFIRST -> try parsing time before date [not default]
	PREFER_PAST -> when year or day of week is ambigueous, assume past
	PREFER_FUTURE -> when year or day of week is ambigueous, assume future
	SUBSECOND -> parse fraction seconds
	VALIDATE -> only accept normal values for HHMMSS, YYMMDD.  Otherwise
		days like -1 might give the last day of the previous month.

=head1 DATE FORMATS RECOGNIZED

=head2 Absolute date formats

	Dow, dd Mon yy
	Dow, dd Mon yyyy
	Dow, dd Mon
	dd Mon yy
	dd Mon yyyy
	Month day{st,nd,rd,th}, year
	Month day{st,nd,rd,th}
	Mon dd yyyy
	yyyy/mm/dd
	yyyy/mm
	mm/dd/yy
	mm/dd/yyyy
	mm/yy
	yy/mm      (only if year > 12, or > 31 if UK)
	yy/mm/dd   (only if year > 12 and day < 32, or year > 31 if UK)
	dd/mm/yy   (only if UK, or an invalid mm/dd/yy or yy/mm/dd)
	dd/mm/yyyy (only if UK, or an invalid mm/dd/yyyy)
	dd/mm      (only if UK, or an invalid mm/dd)

=head2 Relative date formats:

	count "days"
	count "weeks"
	count "months"
	count "years"
	Dow "after next"
	Dow 			(requires PREFER_PAST or PREFER_FUTURE)
	"next" Dow
	"tomorrow"
	"today"
	"yesterday"
	"last" dow
	"last week"
	"now"
	"now" "+" count units
	"now" "-" count units
	"+" count units
	"-" count units
	count units "ago"

=head2 Absolute time formats:

	hh:mm:ss[.ddd] 
	hh:mm 
	hh:mm[AP]M
	hh[AP]M
	hhmmss[[AP]M] 
	"noon"
	"midnight"

=head2 Relative time formats:

	count "minuts"
	count "seconds"
	count "hours"
	"+" count units
	"+" count
	"-" count units
	"-" count
	count units "ago"

=head2 Timezone formats:

	[+-]dddd
	GMT[+-]d+
	[+-]dddd (TZN)
	TZN

=head2 Special formats:

	[ d]d/Mon/yyyy:hh:mm:ss [[+-]dddd]
	yy/mm/dd.hh:mm

=head1 DESCRIPTION

This module recognizes the above date/time formats.   Usually a
date and a time are specified.  There are numerous options for 
controlling what is recognized and what is not.

The return code is always the time in seconds since January 1st, 1970
or undef if it was unable to parse the time.

If a timezone is specified it must be after the time.  Year specifications
can be tacked onto the end of absolute times.

If C<parsedate()> is called from array contect, then it will return two
elements.  On sucessful parses, it will return the seconds and what 
remains of its input string.  On unsucessful parses, it will return
C<undef> and an error string.

=head1 EXAMPLES

	$seconds = parsedate("Mon Jan  2 04:24:27 1995");
	$seconds = parsedate("Tue Apr 4 00:22:12 PDT 1995");
	$seconds = parsedate("04.04.95 00:22", ZONE => PDT);
	$seconds = parsedate("Jan 1 1999 11:23:34.578", SUBSECOND => 1);
	$seconds = parsedate("122212 950404", ZONE => PDT, TIMEFIRST => 1);
	$seconds = parsedate("+3 secs", NOW => 796978800);
	$seconds = parsedate("2 months", NOW => 796720932);
	$seconds = parsedate("last Tuesday");

	($seconds, $remaining) = parsedate("today is the day");
	($seconds, $error) = parsedate("today is", WHOLE=>1);

=head1 AUTHOR

David Muir Sharnoff <muir@idiom.com>.  

=head1 LICENSE

Copyright (C) 1996-1999 David Muir Sharnoff.  License hereby
granted for anyone to use, modify or redistribute this module at
their own risk.  Please feed useful changes back to muir@idiom.com.

