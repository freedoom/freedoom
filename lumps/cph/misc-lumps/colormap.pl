#!/usr/bin/perl -w
# Takes PLAYPAL as input (filename is the only parameter)
# Produces a light graduated COLORMAP on stdout
# O(n^2)
#
# Copyright (C) 2001  Colin Phipps <cphipps@doomworld.com>
# Parts copyright (C) 1999 by id Software (http://www.idsoftware.com/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

use strict;
 
my @colours;

# Return palette read from named file
sub read_palette ($) {
  {
    my $palf = shift;
    open(PALF,"<$palf") or die "failed to open PLAYPAL: $!";
  }
  @colours = ();
  foreach my $i (0..255) {
    my $e;
    read PALF,$e,3;
    push @colours,[unpack("CCC",$e)];
  }
  close PALF;
  return \@colours;
}

sub sq($) { my $x = shift; $x*$x }

# Return closest palette entry to the given RGB triple
sub search_palette {
  my ($r,$g,$b) = @_;
  my $d = 100000; my $n = -1;
  my $i = 0;
  foreach my $c (@colours) {
    my $thisdist = sq($c->[0] - $r) + sq($c->[1] - $g) + sq($c->[2] - $b);
    if ($thisdist < $d) { $d = $thisdist; $n = $i; }
    $i++;
  }
  die "failed to find any close colour?" if $n == -1;
  return $n;
}

sub darkenedpalette($) {
  my $darkensub = shift;
  my @pal;
  foreach my $c (@colours) {
    my @d = $darkensub->(@$c);
    push @pal,search_palette(@d);
  }
  return \@pal;
}

sub makedarkenrgbbyfactor($) {
  my $f = shift;
  return sub { my ($r,$g,$b) = @_; return (int($r*$f),int($g*$f),int($b*$f)) };
}

read_palette(shift @ARGV);
foreach my $i (0..31) {
  my $p = darkenedpalette( makedarkenrgbbyfactor((32.0-$i)/32.0));
  print map { pack("C",$_) } @$p;
  print STDERR ".";
}
print STDERR "\n";
# And now INVERSECOLORMAP
{
  my $p = darkenedpalette(
  sub {
    my ($r,$g,$b) = @_;
    my $x = int (256 - ($r+$g+$b)/3);
    return ($x,$x,$x);
  }
      );
  print map { pack("C",$_) } @$p;
}
