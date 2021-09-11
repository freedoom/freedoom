playpal.lmp: playpal-base.lmp playpal
	./playpal playpal-base.lmp > playpal.lmp
	cp playpal.lmp ../

doom.gpl: playpal-base.lmp
	./gen-gimp-palette

clean:
	$(RM) playpal.lmp ../playpal.lmp
	$(RM) doom.gpl

.PHONY: clean
