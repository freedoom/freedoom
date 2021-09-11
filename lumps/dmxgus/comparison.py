# SPDX-License-Identifier: BSD-3-Clause
#
# Generate comparison MIDI file.
#
# The comparison MIDI is used for testing and tweaking the similarity
# groups in the configuration file. In each group, the instruments in
# the group should sound broadly similar, and the first in the group
# should be able to substitute for any member of the group.
#
# Each similarity group is played in order, with a pause between each
# instrument. A programme of the instruments is printed to stdout so
# that the user can identify each instrument in order.
#
# To use the comparison MIDI, use a port that supports Timidity for
# MIDI playback, and configure it to use the GUS patch set (use
# music/dgguspat.zip from the idgames archive). Use the "full"
# configuration file (timidity.cfg in the .zip) so that every
# instrument is used for playback. Rename comparison.mid to
# d_runnin.lmp and run with '-file d_runnin.lmp -warp 1', so that the
# music plays.


from config import *
import midi


def instrument_num(instrument):
    """Given a GUS patch name, get the MIDI instrument number.

       For percussion instruments, the instrument number is offset
       by 128.
    """
    for key, name in GUS_INSTR_PATCHES.items():
        if name == instrument:
            return key
    raise Exception("Unknown instrument %s" % instrument)


pattern = midi.Pattern(resolution=48)
track = midi.Track()
track.append(midi.ControlChangeEvent(tick=0, channel=9, data=[7, 92]))

time = 500
for group in SIMILAR_GROUPS:
    # Don't bother with special effects.
    # if group[0] == 'blank':
    #   continue

    print("Group: ")
    empty = True
    for instrument in group:
        inum = instrument_num(instrument)

        # For normal instruments, play a couple of different notes.
        # For percussion instruments, play a couple of note on
        # the percussion channel.
        if inum <= 128:
            print("\t%s (%i)" % (instrument, inum))
            track.extend(
                [
                    midi.ProgramChangeEvent(tick=time, channel=0, data=[inum]),
                    midi.NoteOnEvent(
                        tick=0, channel=0, velocity=92, pitch=midi.A_3
                    ),
                    midi.NoteOffEvent(
                        tick=50, channel=0, velocity=92, pitch=midi.A_3
                    ),
                    midi.NoteOnEvent(
                        tick=0, channel=0, velocity=92, pitch=midi.B_3
                    ),
                    midi.NoteOffEvent(
                        tick=50, channel=0, velocity=92, pitch=midi.B_3
                    ),
                ]
            )
        else:
            print("\t%s (percussion %i)" % (instrument, inum - 128))
            track.extend(
                [
                    midi.NoteOnEvent(
                        tick=time, channel=9, velocity=92, pitch=inum - 128
                    ),
                    midi.NoteOffEvent(tick=50, channel=9, pitch=inum - 128),
                    midi.NoteOnEvent(
                        tick=0, channel=9, velocity=92, pitch=inum - 128
                    ),
                    midi.NoteOffEvent(tick=50, channel=9, pitch=inum - 128),
                ]
            )

        empty = False
        time = 100

    if not empty:
        time = 500

# Four drumbeats indicate the end of the track and that the music is
# going to loop.
for i in range(4):
    track.extend(
        [
            midi.NoteOnEvent(tick=20, channel=9, velocity=92, pitch=35),
            midi.NoteOffEvent(tick=20, channel=9, pitch=35),
        ]
    )

track.append(midi.EndOfTrackEvent(tick=1))
pattern.append(track)

# Save the pattern to disk
midi.write_midifile("comparison.mid", pattern)
