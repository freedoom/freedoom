#!/usr/bin/env python
#
# Find duplicated music tracks and create a summary report of music
# that the project needs.

from glob import glob
import os
import re
import sys

PHASE1_MATCH_RE = re.compile(r'(e\dm\d)', re.I)
PHASE2_MATCH_RE = re.compile(r'(map\d\d)', re.I)
FREEDM_MATCH_RE = re.compile(r'(dm\d\d)', re.I)

DOOM2_TRACKS = (
	'runnin', 'stalks', 'countd', 'betwee', 'doom', 'the_da', 'shawn',
	'ddtblu', 'in_cit', 'dead', 'stlks2', 'theda2', 'doom2', 'ddtbl2',
	'runni2', 'dead2', 'stlks3', 'romero', 'shawn2', 'messag', 'count2',
	'ddtbl3', 'ampie', 'theda3', 'adrian', 'messg2', 'romer2', 'tense',
	'shawn3', 'openin', 'evil', 'ultima',
)

def get_music_tracks():
	"""Returns a dictionary mapping from MIDI name (subpath of musics/)
	   to a list of game tracks that use that MIDI."""
	result = {}
	musics_path = os.path.join(os.path.dirname(sys.argv[0]), '../musics')
	for mus in glob('%s/*.mus' % musics_path):
		try:
			symlink = os.readlink(mus)
			if symlink not in result:
				result[symlink] = []
			result[symlink].append(os.path.basename(mus))
		except OSError:
			pass
	return result

def doom2_level_for_file(filename):
	"""Given a filename that may be named like a Doom 2 music name
	   (eg. d_stalks.mid), get the level number it corresponds to
	   or 0 if it doesn't match."""
	filename = os.path.basename(filename)
	for i, doom2_name in enumerate(DOOM2_TRACKS):
		if filename.startswith('d_%s.' % doom2_name):
			return i + 1
	else:
		return 0

def get_prime_track(midi, tracks):
	"""Given a list of tracks that all use the same MIDI, find the
	   "prime" one (the one that isn't a reuse/duplicate)."""
	# We have almost all Phase 2 tracks fulfilled. So if the same
	# track is used in Phase 1 and Phase 2, or Phase 2 and FreeDM,
	# the Phase 2 track is probably the leader.
	phase2_tracks = [x for x in tracks if PHASE2_MATCH_RE.search(x)]
	if len(phase2_tracks) == 1:
		return phase2_tracks[0]

	level = doom2_level_for_file(midi)
	if level:
		for track in phase2_tracks:
			if ('map%02i' % level) in track:
				return track

	# If the filename of the MIDI file (symlink target) describes a
	# level, then that level is the leader.
	m = PHASE1_MATCH_RE.search(os.path.basename(midi))
	if m:
		level = m.group(1)
		for track in tracks:
			if level in track:
				return track

	# We're out of options. Pick the first one in the list.
	#print 'Warning: Don't know which of %s is the leader for %s.' % (
	#	tracks, midi)
	return tracks[0]

def find_missing_tracks(tracks):
	"""Given a dictionary of tracks, get a list of "missing" tracks."""
	result = []
	for midi, tracks in tracks.items():
		if len(tracks) < 2:
			continue
		prime_track = get_prime_track(midi, tracks)
		result.extend(x for x in tracks if x != prime_track)
	return result

def tracks_matching_regexp(tracks, regexp):
	return set([x for x in tracks if regexp.search(x)])

def print_report(title, tracks):
	if len(tracks) == 0:
		return
	print(title)
	for track in sorted(tracks):
		print('\t%s' % track.replace('.mus', '').upper())
	print('')

missing_tracks = set(find_missing_tracks(get_music_tracks()))
phase1_tracks = tracks_matching_regexp(missing_tracks, PHASE1_MATCH_RE)
phase2_tracks = tracks_matching_regexp(missing_tracks, PHASE2_MATCH_RE)
freedm_tracks = tracks_matching_regexp(missing_tracks, FREEDM_MATCH_RE)
other_tracks = missing_tracks - phase1_tracks - phase2_tracks - freedm_tracks

print('=== Missing tracks (tracks currently using duplicates):\n')
print_report('Phase 1 tracks:', phase1_tracks)
print_report('Phase 2 tracks:', phase2_tracks)
print_report('FreeDM tracks:', freedm_tracks)
print_report('Other tracks:', other_tracks)

