all             :       playpal.lmp colormap.lmp

playpal.lmp	:	playpal-base.lmp playpal.py
	./playpal.py playpal-base.lmp > playpal.lmp

colormap.lmp	:	playpal.lmp colormap.py
	./colormap.py playpal.lmp > colormap.lmp

SOURCES=playpal.py colormap.py COPYING Makefile
VERSION=0.0.1

dist		:	doom-misc-lumps-$(VERSION).tar.gz

doom-misc-lumps-$(VERSION).tar.gz       :       $(SOURCES)
	tar czf $@ $(SOURCES)

clean:
	rm -f playpal.lmp colormap.lmp doom-misc-lumps-$(VERSION).tar.gz

.PHONY  :       dist clean
