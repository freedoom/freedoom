#!/usr/bin/perl -w
# Script to generate the PLAYPAL lump used by the Doom engine, specifically the
# which contains 14 alternative palettes which are used for various
# environmental effects. The base palette from which these are derived is either
# generated, or taken from a file.
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

# IHS (Intensity Hue Saturation) to RGB conversion, utility function
#
# Obtained from a web page, which credited the following for the algorithm
#  Kruse, F.A. and G.L. Raines, 1984. "A Technique For Enhancing Digital
#  Colour Images by Contrast Stretching in Munsell Colour Space",
#  Proceedings of the International Symposium on Remote Sensing of
#  Environment, 3rd Thematic Conference, Environmental Research Institute
#  of Michigan, Colorado Springs, Colorado, pp. 755-773.
#  Bonham-Carter, Graeme F., 1994.  Geographic Informations Systems for
#  Geoscientists: Modelling with GIS. Computer Methods in the
#  Geosciences, Volume 13, published by Pergamon (Elsevier Science Ltd),
#  pp. 120-125.

use constant R2 => 1 / sqrt(2);
use constant R3 => 1 / sqrt(3);
use constant R6 => 1 / sqrt(6);
use constant PI => 3.141592;

sub ihs_to_rgb($$$)
{
  my ($i,$h,$s) = @_;
# Hue and Saturation values are unscaled first:
  $i = $i * (422/255);
  $h = $h * (2 * PI / 255);
  $s = $s * ("208.2066" / 255);
  my ($b,$x) = ($s * cos $h, $s * sin $h);
  return
    [ 
    R3 * $i - R6 * $b - R2 * $x,
    R3 * $i - R6 * $b + R2 * $x,
    R3 * $i + 2 * R6 * $b,
    ];
}

# New palette builder

sub make_pal_range($$$$)
{
  my ($i,$h,$s,$n) = @_;
  my @r = map { ihs_to_rgb($i*(1 + $n - $_)/$n,$h,$s*(1 + $n - $_)/$n) } (1..$n);
  die unless @r == $n;
  return @r;
}

# Very crude traversal of the IHS colour ball

sub make_palette_new ()
{
  my @p = (
  make_pal_range(255,0,0,32),
  ( map { make_pal_range(127,171+$_*256/7,255,16) } (1..7) ),
  ( map { make_pal_range(256,$_*256/7,127,16) } (1..7) )
  );
  return \@p;
}

# Return palette read from named file
sub read_palette ($) {
  {
    my $palf = shift;
    open(PALF,"<$palf") or die "failed to open PLAYPAL: $!";
  }
  my @colours = ();
  foreach my $i (0..255) {
    my $e;
    read PALF,$e,3;
    push @colours,[unpack("CCC",$e)];
  }
  close PALF;
  return \@colours;
}

sub make_palette ()
{
  my $palf = shift @ARGV;
  return $palf ? read_palette($palf) : make_palette_new;
}

# Old palette builder
#sub make_pal_range($$$$$$)
#{
#  my ($rs,$gs,$bs,$re,$ge,$be) = @_;
#  return map { my $e = $_/16; my $s = 1-$e;
#  [$rs*$s + $re*$e, $gs*$s + $ge*$e, $bs*$s + $be * $e] } (1..16);
#}
#
#sub make_palette ()
#{
#  my @p = (
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(255,255,255,255,0,0), # pinks
#  make_pal_range(255,0,0,0,0,0), # dull reds
#  make_pal_range(255,128,255,192,192,0), # yellows
#  make_pal_range(255,255,0,0,0,0), # yellows
#  make_pal_range(255,255,255,0,0,0), # white
#  make_pal_range(127,127,127,0,0,0), # gray
#  make_pal_range(255,255,255,0,255,0), # light greens
#  make_pal_range(0,255,0,0,0,0), # greens
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(0,0,255,0,0,0), # dark blues
#  make_pal_range(255,255,255,0,0,255), # bright blues
#  make_pal_range(255,0,255,0,0,0), # magenta
#  make_pal_range(0,255,255,0,0,0), # cyan
#  make_pal_range(0,0,0,0,0,0), # hmmm
#  make_pal_range(0,0,0,0,0,0)); # hmmm
#  return \@p;
#}

# Now the PLAYPAL stuff - take the main palette and construct biased versions
# for the palette translation stuff
sub bias_towards($$$) {
  my ($rgb,$target,$p) = @_;
  my (@r,$i);
  for ($i=0; $i<3; $i++) { $r[$i] = $rgb->[$i]*(1-$p) + $target->[$i]*$p }
  return \@r;
}

sub modify_palette_per_entry($$)
{
  my $palref = shift;
  my $efunc = shift;
  my @newpal = map { $efunc->($_) } @$palref; 
  return \@newpal;
}

# Encode palette in the 3-byte RGB triples format expected by the engine
sub clamp_pixval ($)
{
  my $v = int shift; 
  return ($v < 0) ? 0 : ($v > 255) ? 255 : $v;
}

sub encode_palette
{
  my $p = shift;
  return join("",map { pack("CCC", map { clamp_pixval $_ } @$_) } @$p);
}

# From st_stuff.c, Copyright 1999 id Software, license GPL
#define STARTREDPALS         1
#define STARTBONUSPALS       9
#define NUMREDPALS           8
#define NUMBONUSPALS         4
#define RADIATIONPAL         13

my @needed_palettes = (
# Normal palette
  sub { shift; },
# STARTREDPALS
  (map {
    my $p = $_*1/8;
    sub {
      modify_palette_per_entry(shift,
          sub { bias_towards(shift, [255,0,0],$p) }
                              )
    }
  } (1..8)),
# STARTBONUSPALS
  (map {
    my $p = $_*0.4/4;
    sub {
      modify_palette_per_entry(shift,
          sub { bias_towards(shift, [128,128,128],$p) }
                              )
    }
  } (1..4)),
# RADIATIONPAL
  sub {
    modify_palette_per_entry(shift,
        sub { bias_towards(shift, [0,255,0],0.2) }
                            )
  }
);

# Main program - make a base palette, then do the biased versions
my $pal = make_palette;

print map { encode_palette(&$_($pal)) } @needed_palettes;

