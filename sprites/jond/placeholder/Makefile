# generates placeholder sprites for monsters
#
SPRITEDIR = ../..

# use the AOD skeleton for humanoid monsters
SKELDIR   = $(SPRITEDIR)/linguica/aoddoom_skeletons
SKELSRC   = $(wildcard $(SKELDIR)/sarg*)
VILEDEST  = $(notdir $(SKELSRC))

# use the arachnotron for the spiderdemon
BSPISRC   = $(wildcard $(SPRITEDIR)/bspi*)
SPIDDEST  = $(notdir $(BSPISRC))

# use the baron for the HK
BOSSSRC   = $(wildcard $(SPRITEDIR)/boss*)
BOS2DEST  = $(notdir $(BOSSSRC))

# use the caco for the pain elemental
HEADSRC   = $(wildcard $(SPRITEDIR)/head*) 
PAINDEST  = $(notdir $(HEADSRC))

DUMMY     =../../dummy.gif
# TODO: if dst's width is < src's, src is clipped. Try to prevent this.
ARGS=-compose src-over -gravity center
TARGETS    = $(SPIDDEST) $(BOS2DEST) $(PAINDEST)

foo: $(VILEDEST) $(TARGETS)

clean:
	rm -f $(VILEDEST) $(TARGETS)

$(TARGETS): $(DUMMY) Makefile
	composite $(ARGS) $(DUMMY) $(SPRITEDIR)/$@ $@

# special case since the source isn't in $(SPRITEDIR)
$(VILEDEST): $(DUMMY) Makefile
	composite $(ARGS) $(DUMMY) $(SKELDIR)/$@ $@

test:
	echo $(BSPISRC)
.PHONY: foo clean
