SRCDIR=../../linguica/aoddoom_skeletons
SRCSPRITES= $(wildcard $(SRCDIR)/sarg*)
DSTSPRITES= $(notdir $(SRCSPRITES))
DUMMY=../../dummy.gif
# TODO: if dst's width is < src's, src is clipped. Try to prevent this.
ARGS=-compose src-over -gravity center

foo: $(DSTSPRITES)

clean:
	rm -f $(DSTSPRITES)

$(DSTSPRITES): $(DUMMY) Makefile
	composite $(ARGS) $(DUMMY) $(SRCDIR)/$@ $@

.PHONY: foo clean
