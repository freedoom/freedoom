#!/usr/bin/env perl
# 
# perform sanity check on assignments lists; make sure everything in
# the deutex tree is listed in the assignment lists

sub sanitycheck {
	my ($dir, $file) = @_;

    print "Checking $dir\n";

	open(LIST_FILE, $file) or die "cant open $file";

	while (<LIST_FILE>) {
		chomp;
		
		next if /^\s*$/ or /^\#/;

		/^(\w+)/;
		my $lumpname = $1;

		my @files;

		if ($dir eq 'musics') {
			@files = glob("$dir/d_$lumpname*");
		} else {
			@files = glob("$dir/$lumpname*");
		}

		if (/done/ or /in dev/) {
			if (scalar @files <= 0) {
				print "$dir: files not found for $lumpname\n";
			}
		} else {
			if (scalar @files > 0) {
				print "$dir: files found for $lumpname\n";
			}
		}
	}

	close(LIST_FILE);
}

my $status_dir = "status";

sanitycheck 'sprites', "$status_dir/sprites_list";
sanitycheck 'patches', "$status_dir/patches_list";
sanitycheck 'flats', "$status_dir/flats_list";
sanitycheck 'graphics', "$status_dir/graphics_list";
sanitycheck 'sounds', "$status_dir/sounds_list";
#sanitycheck 'musics', "$status_dir/musics_list";

