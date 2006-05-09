#!/usr/bin/perl
#
# extract graphic offsets for graphics and sprites 
# replace entries in the shareware wadinfo.txt with the appropriate
# lines from the main wadinfo.txt

open(WADINFO, "wadinfo.txt.in") or die "cant open wadinfo.txt";

my %resdata;
my $grafmode = 0;

while(<WADINFO>) {
	chomp;

	s/\#.*$//; # comments
	next if (/^\s*$/);

	if (/\[.*\]/) {
		my $section = $_;
		$section =~ s/\[(.*)\]/$1/;
		$grafmode = $section eq "graphics" || $section eq "sprites";
	} elsif ($grafmode) {
		$sprname = lc $_;
		$sprname =~ s/\s.*$//;
		$resdata{$sprname} = $_;
	}
}

close(WADINFO);

open(WADINFO, "wadinfo_sw.txt.in.in") or die "cant open wadinfo_sw.txt";

while (<WADINFO>) {
	chomp;

	if (/\s*\#.*$/ || /^\s*$/) {
	} elsif (/\[.*\]/) {
		my $section = $_;
		$section =~ s/\[(.*)\]/$1/;
		$grafmode = $section eq "graphics" || $section eq "sprites";
	} elsif ($grafmode) {
		$sprname = lc $_;
		$sprname =~ s/\s.*$//;
		if ($resdata{$sprname}) {
		   $_ = $resdata{$sprname} . "\t\t# forwarded from wadinfo.txt";
		}
	}

	print "$_\n";
}

close(WADINFO);

