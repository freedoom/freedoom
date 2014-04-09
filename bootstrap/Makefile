# Build a fake IWAD to bootstrap deutex

IWAD=./doom2.wad

$(IWAD): ../lumps/cph/misc-lumps/playpal-base.lmp
	./bootstrap.py < $< > $@

clean:
	rm -f $(IWAD)

.PHONY: clean
