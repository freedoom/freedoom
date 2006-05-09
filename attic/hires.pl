#!/usr/bin/perl
#
# front end part of the hires patch->texture convertor to be
#

use strict;

my %textures;
my %patches;

sub file_date {
	my ($file) = @_;

	return 0;
}

sub get_patches {
	open(PATCHES, "textures/patchsizes") or die "cant open patchsizes";

	%patches = {};

	foreach (<PATCHES>) {
		chomp;
		my @fields = split(/\s+/);
		my $file = "patches_hi/$fields[0].png";
		my $newpatch = {
			name => $fields[0],
			width => $fields[1],
			height => $fields[2],
			file => $file,
			exists => -e $file,
			date => file_date($file)+1,
		};

		# store in hash

		$patches{$fields[0]} = $newpatch;
	}

	close(PATCHES);
}

sub get_textures {
	open(TEXTURES, "textures/combined/texture1.txt") or die "cant open texture1.txt";

	%textures = {};

	my $curtext = undef;

	foreach(<TEXTURES>) {
		chomp;
		next if (/^\#/ || /^\;/ || /^\s*$/);
		$_ = lc $_;

		my @fields = split(/\s+/);

		if ($fields[0] eq "\*") {
			# another patch
			
			my $newpatch = {
				patch => $patches{$fields[1]},
				x => $fields[2],
				y => $fields[3],
			};

			my $curpatches = $curtext->{patches};

			push(@$curpatches, $newpatch);
		} else {
			# new texture

			my $file = "patches_hi/.tga/$fields[0]";
			my $patchlist = [];

			$curtext = {
				name => $fields[0],
				file => $file,
				width => $fields[1],
				height => $fields[2],
				date => file_date($file),
				patches => $patchlist,
			};

			# get file date of existing file?

			$textures{$fields[0]} = $curtext;
		}
	}

	close(TEXTURES);
}

sub build_texture {
	my ($this) = @_;
	
	print "build texture $this->{name}\n";
}

sub dep_loop {
	mainloop: foreach (keys %textures) {
		my $this = $textures{$_};
		my $patchlist = $this->{patches};
		my $uptodate = 1;

		#print "$_: " . @$patchlist . "\n";

		foreach (@$patchlist) {
			#print $this->{name} . " : " . $_->{patch}->{name} . "\n";
			if (!$_->{patch}->{exists}) {
				# a patch is missing, cant build this
			
				#print $this->{name} . ": patch missing\n";
				next mainloop;
			}
			if ($_->{patch}->{date} > $this->{date}) {

				# if the date of one of the patches is
				# newer than the date of the produced
				# texture file, this is not up to date

				$uptodate = 0;
			}
		}

		if (!$uptodate) {
			build_texture($this);
		} else {
			#print $this->{name} . ": up to date\n";
		}
	}
}

get_patches;
get_textures;
dep_loop;
