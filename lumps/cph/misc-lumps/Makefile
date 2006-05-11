all             :       playpal.lmp colormap.lmp

playpal.lmp	:	playpal-base.lmp playpal.pl
	./playpal.pl playpal-base.lmp > playpal.lmp

colormap.lmp	:	playpal.lmp colormap.pl
	./colormap.pl playpal.lmp > colormap.lmp

SOURCES=playpal.pl colormap.pl COPYING Makefile
VERSION=0.0.1

dist		:	doom-misc-lumps-$(VERSION).tar.gz

doom-misc-lumps-$(VERSION).tar.gz       :       $(SOURCES)
	tar czf $@ $(SOURCES)

.PHONY  :       all dist
