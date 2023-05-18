all: playpal.lmp newpal.lmp

# So that Deutex can merge it
newpal.lmp: playpal-new.lmp playpal
	./playpal playpal-new.lmp > newpal.lmp
	cp newpal.lmp ../

playpal.lmp: playpal-base.lmp playpal
	./playpal playpal-base.lmp > playpal.lmp
	cp playpal.lmp ../

doom.gpl: playpal-base.lmp
	./gen-gimp-palette

clean:
	$(RM) newpal.lmp ../newpal.lmp
	$(RM) playpal.lmp ../playpal.lmp
	$(RM) doom.gpl

.PHONY: clean
