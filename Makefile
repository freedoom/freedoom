# SPDX-License-Identifier: BSD-3-Clause

VERSION=$(shell git describe --dirty 2>/dev/null || cat VERSION)
WADS=wads
CPP=scripts/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-v0 -rate accept
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

FREEDOOM1=$(WADS)/freedoom1.wad
FREEDOOM2=$(WADS)/freedoom2.wad
FREEDM=$(WADS)/freedm.wad

OBJS=$(FREEDM) $(FREEDOOM1) $(FREEDOOM2)

all: $(OBJS)

subdirs:
	$(MAKE) -C graphics/text
	$(MAKE) VERSION=$(VERSION) -C graphics/titlepic
	$(MAKE) -C lumps/playpal
	$(MAKE) -C lumps/colormap
	$(MAKE) -C lumps/genmidi
	$(MAKE) -C lumps/dmxgus
	$(MAKE) -C lumps/textures
	$(MAKE) -C bootstrap


# this is a useless dependency to force builds

force:

lumps/freedoom.lmp lumps/freedm.lmp: force
	echo $(VERSION) > $@

# update wadinfo.txt

wadinfo.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DDOOM2 < $< | scripts/wadinfo-builder.py > $@
wadinfo_phase1.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DDOOM1 -DULTDOOM < $< | scripts/wadinfo-builder.py -dummy > $@
wadinfo_phase2.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DDOOM2 < $< | scripts/wadinfo-builder.py -dummy > $@
wadinfo_freedm.txt : buildcfg.txt subdirs lumps/freedoom.lmp lumps/freedm.lmp
	$(CPP) -P -DFREEDM < $< | scripts/wadinfo-builder.py -dummy > $@

# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to whichever wad we are working on

#---------------------------------------------------------
# freedm iwad

$(FREEDM): wadinfo_freedm.txt subdirs
	@mkdir -p $(WADS)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_freedm.txt $@

#---------------------------------------------------------
# phase 1 (udoom) iwad

$(FREEDOOM1): wadinfo_phase1.txt subdirs
	@mkdir -p $(WADS)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase1.txt $@

#---------------------------------------------------------
# phase 2 (doom2) iwad

$(FREEDOOM2): wadinfo_phase2.txt subdirs
	@mkdir -p $(WADS)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase2.txt $@

%.html: %.adoc
	TZ=UTC asciidoc $<

doc: $(patsubst %.adoc,%.html,$(wildcard *.adoc))

COPYING.txt: COPYING.adoc
	unix2dos --add-bom --newfile $< $@

CREDITS.txt: CREDITS
	unix2dos --add-bom --newfile $< $@

DISTDOCS=COPYING.txt CREDITS.txt README.html

.PHONY: dist

# Due to convoluted reasons, the WADs must directly proceed the game name.
dist: $(OBJS) COPYING.txt CREDITS.txt README.html
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedm $(FREEDM) $(DISTDOCS)
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedoom $(FREEDOOM1) $(FREEDOOM2) $(DISTDOCS)

json: $(OBJS)
ifndef JSON
	@echo "Define JSON as the file to output." >&2
	@exit 1
else
	JSON=$(JSON) VERSION=$(VERSION) scripts/makejson
endif

clean:
	rm -f	*.html deutex.log $(OBJS) \
		./COPYING.txt ./CREDITS.txt \
		./wadinfo.txt ./wadinfo_phase1.txt \
		./wadinfo_phase2.txt ./wadinfo_freedm.txt \
		./lumps/freedoom.lmp \
		./lumps/freedm.lmp
	-rmdir $(WADS)

	$(MAKE) -C dist clean
	$(MAKE) -C graphics/text clean
	$(MAKE) -C graphics/titlepic clean
	$(MAKE) -C lumps/playpal clean
	$(MAKE) -C lumps/colormap clean
	$(MAKE) -C lumps/genmidi clean
	$(MAKE) -C lumps/dmxgus clean
	$(MAKE) -C lumps/textures clean
	$(MAKE) -C bootstrap clean

prefix?=/usr/local
bindir?=/bin
mandir?=/share/man
waddir?=/share/games/doom
target=$(DESTDIR)$(prefix)

%.6:
	$(MAKE) -C dist man-$*

%.png:
	$(MAKE) -C dist icon-$*

install-%: $(WADS)/%.wad %.6 %.png
	install -Dm 755 dist/freedoom "$(target)$(bindir)/$*"
	install -Dm 644 dist/$*.6 -t "$(target)$(mandir)/man6"
	install -Dm 644 $(WADS)/$*.wad -t "$(target)$(waddir)"
	install -Dm 644 dist/$*.desktop -t "$(target)/share/applications"
	install -Dm 644 dist/$*.appdata.xml -t "$(target)/share/appdata"
	install -Dm 644 dist/$*.png -t "$(target)/share/icons"

uninstall-%:
	rm "$(target)$(bindir)/$*"
	rm "$(target)$(mandir)/man6/$*.6"
	rm "$(target)$(waddir)/$*.wad"
	rm "$(target)/share/applications/$*.desktop"
	rm "$(target)/share/appdata/$*.appdata.xml"
	rm "$(target)/share/icons/$*.png"
	-rmdir -p "$(target)$(bindir)"
	-rmdir -p "$(target)$(mandir)/man6"
	-rmdir -p "$(target)$(waddir)"
	-rmdir -p "$(target)/share/applications"
	-rmdir -p "$(target)/share/appdata"
	-rmdir -p "$(target)/share/icons"

install: install-freedm install-freedoom1 install-freedoom2

uninstall: uninstall-freedm uninstall-freedoom1 uninstall-freedoom2
