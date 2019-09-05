# Build a fake IWAD to bootstrap deutex

IWAD=./doom2.wad

$(IWAD): ../lumps/playpal/playpal-base.lmp
	./bootstrap < $< > $@

clean:
	$(RM) $(IWAD)

.PHONY: clean
