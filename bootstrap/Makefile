# Build a fake IWAD to bootstrap deutex

IWAD=./doom2.wad

$(IWAD): ../lumps/playpal/playpal-base.lmp
	./bootstrap.py < $< > $@

clean:
	rm -f $(IWAD)

.PHONY: clean
