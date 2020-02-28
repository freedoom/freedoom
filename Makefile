# SPDX-License-Identifier: BSD-3-Clause

VERSION=$(shell git describe --abbrev=8 --dirty 2>/dev/null || echo v0.12.1)
WADS=wads
ASCIIDOC=asciidoc
ADOCOPTS=--backend=html5 --conf-file=.adoc-layout.conf
ASCIIDOC_MAN=a2x -f manpage
CPP=scripts/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-v0 -rate accept
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/
NODE_BUILDER=ZenNode
NODE_BUILDER_LEVELS=c?m? dm?? map??

FREEDOOM1=$(WADS)/freedoom1.wad
FREEDOOM2=$(WADS)/freedoom2.wad
FREEDM=$(WADS)/freedm.wad

OBJS=$(FREEDM) $(FREEDOOM1) $(FREEDOOM2)

.PHONY: clean dist

all: deutex-check $(OBJS)

subdirs:
	$(MAKE) -C lumps/dehacked # graphics/text depends on generated dehacked files
	$(MAKE) VERSION=$(VERSION) -C graphics/text
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

# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to whichever wad we are working on

#---------------------------------------------------------
# Build checks

# Make sure deutex supports PNG
deutex-check:
	@$(DEUTEX) -h | grep -qw PNG || { \
	echo "$(DEUTEX) does not support PNG. Try building deutex with the PNG"; \
	echo "libraries (libpng and libpng-devel or similar packages) installed."; \
	echo "deutex can be downloaded from https://github.com/Doom-Utils/deutex."; \
	echo "The full path to duetex can be specified by passing"; \
	echo "DEUTEX=/the/path/to/deutex to make when building Freedoom."; \
	exit 1; }

#---------------------------------------------------------
# freedm iwad

wadinfo_freedm.txt : buildcfg.txt subdirs lumps/freedoom.lmp lumps/freedm.lmp
	$(CPP) -P -DFREEDM < $< > $@

$(FREEDM): wadinfo_freedm.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_freedm.txt $@

#---------------------------------------------------------
# phase 1 (udoom) iwad

wadinfo_phase1.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DPHASE1 < $< > $@

$(FREEDOOM1): wadinfo_phase1.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase1.txt $@

#---------------------------------------------------------
# phase 2 (doom2) iwad

wadinfo_phase2.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DPHASE2 < $< > $@

$(FREEDOOM2): wadinfo_phase2.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase2.txt $@

%.html: %.adoc
	$(ASCIIDOC) $(ADOCOPTS) $<

manual/freedoom-manual.pdf: manual/manual.adoc
	$(MAKE) -C manual

COPYING.txt: COPYING.adoc
	unix2dos --add-bom --newfile $< $@

CREDITS.txt: CREDITS
	unix2dos --add-bom --newfile $< $@

HTMLDOCS=NEWS.html README.html
TEXTDOCS=COPYING.txt CREDITS.txt
DISTDOCS=$(HTMLDOCS) $(TEXTDOCS) manual/freedoom-manual.pdf

dist: $(OBJS) $(DISTDOCS)
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedm $(FREEDM) $(DISTDOCS)
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedoom $(FREEDOOM1) $(FREEDOOM2) $(DISTDOCS)

json: $(OBJS)
ifndef JSON
	@echo "Define JSON as the file to output." >&2
	@exit 1
else
	JSON=$(JSON) VERSION=$(VERSION) scripts/makejson
endif

doom.gpl: lumps/playpal/playpal-base.lmp
	$(MAKE) -C lumps/playpal $@
	mv lumps/playpal/$@ .

gimp-palette: doom.gpl

clean:
	$(RM) *.html doom.gpl $(OBJS) \
	      ./COPYING.txt ./CREDITS.txt \
	      ./wadinfo_phase1.txt \
	      ./wadinfo_phase2.txt \
	      ./wadinfo_freedm.txt \
	      ./lumps/freedoom.lmp \
	      ./lumps/freedm.lmp
	-rmdir $(WADS)

	$(MAKE) -C bootstrap clean
	$(MAKE) -C dist clean
	$(MAKE) -C graphics/text clean
	$(MAKE) -C lumps/dehacked clean
	$(MAKE) -C lumps/playpal clean
	$(MAKE) -C lumps/colormap clean
	$(MAKE) -C lumps/genmidi clean
	$(MAKE) -C lumps/dmxgus clean
	$(MAKE) -C lumps/textures clean
	$(MAKE) -C manual clean

# Test targets all of which are a dependency of "test".

# Test that WAD files have the expected map names.
test-map-names:
	scripts/fix-map-names -t levels

# Run all tests. Add test-* targets above, and then as a dependency here.
test: test-map-names
	@echo
	@echo "All tests passed."

# Non-test targets that run scripts in the "scripts" directory.

# Fix the map names.
fix-map-names:
	scripts/fix-map-names levels

# Rebuild the nodes for the level WADs. By default this invokes "ZenNode" on
# all 100 level WADs. Override the "NODE_BUILDER" prefixed variables to
# configure.
rebuild-nodes: $(addprefix levels/,$(addsuffix .wad,$(NODE_BUILDER_LEVELS)))
	for level in $^; \
	do \
		$(NODE_BUILDER) $$level -o $$level; \
	done

%.6:
	$(MAKE) ASCIIDOC_MAN="$(ASCIIDOC_MAN)" -C dist $@

%.png:
	$(MAKE) -C dist $@

prefix?=/usr/local
bindir?=/bin
docdir?=/share/doc
mandir?=/share/man
waddir?=/share/games/doom
target=$(DESTDIR)$(prefix)

install-freedm: $(FREEDM) $(HTMLDOCS) manual/freedoom-manual.pdf \
                freedm.6 io.github.freedoom.FreeDM.png
	install -Dm 644 dist/io.github.freedoom.FreeDM.desktop \
	                -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.FreeDM.metainfo.xml \
	                -t "$(target)/share/metainfo"
	install -Dm 755 dist/freedoom "$(target)$(bindir)/freedm"
	install -Dm 644 dist/freedm.6 -t "$(target)$(mandir)/man6"
	install -Dm 644 $(FREEDM) -t "$(target)$(waddir)"
	install -Dm 644 dist/io.github.freedoom.FreeDM.png \
	                -t "$(target)/share/icons"
	install -Dm 644 CREDITS NEWS.html README.html -t "$(target)$(docdir)/freedm"
	install -Dm 644 COPYING.adoc "$(target)$(docdir)/freedm/COPYING"
	-install -Dm 644 manual/freedoom-manual.pdf -t "$(target)$(docdir)/freedm"

install-freedoom: $(FREEDOOM1) $(FREEDOOM2) $(HTMLDOCS)                 \
                  manual/freedoom-manual.pdf freedoom1.6 freedoom2.6    \
                  io.github.freedoom.Phase1.png                         \
                  io.github.freedoom.Phase2.png
	install -Dm 644 dist/io.github.freedoom.Phase1.desktop \
	                -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.Phase2.desktop \
	                -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.Phase1.metainfo.xml \
	                -t "$(target)/share/metainfo"
	install -Dm 644 dist/io.github.freedoom.Phase2.metainfo.xml \
	                -t "$(target)/share/metainfo"
	install -Dm 755 dist/freedoom "$(target)$(bindir)/freedoom1"
	install -Dm 755 dist/freedoom "$(target)$(bindir)/freedoom2"
	install -Dm 644 dist/freedoom1.6 -t "$(target)$(mandir)/man6"
	install -Dm 644 dist/freedoom2.6 -t "$(target)$(mandir)/man6"
	install -Dm 644 $(FREEDOOM1) $(FREEDOOM2) -t "$(target)$(waddir)"
	install -Dm 644 dist/io.github.freedoom.Phase1.png \
	                -t "$(target)/share/icons"
	install -Dm 644 dist/io.github.freedoom.Phase2.png \
	                -t "$(target)/share/icons"
	install -Dm 644 CREDITS NEWS.html README.html \
	                -t "$(target)$(docdir)/freedoom"
	install -Dm 644 COPYING.adoc "$(target)$(docdir)/freedoom/COPYING"
	-install -Dm 644 manual/freedoom-manual.pdf -t "$(target)$(docdir)/freedoom"

uninstall-freedm:
	$(RM)                                                                   \
	      "$(target)/share/applications/io.github.freedoom.FreeDM.desktop"  \
	      "$(target)/share/metainfo/io.github.freedoom.FreeDM.metainfo.xml" \
	      "$(target)/share/icons/io.github.freedoom.FreeDM.png"             \
	      "$(target)$(bindir)/freedm"                                       \
	      "$(target)$(mandir)/man6/freedm.6"                                \
	      "$(target)$(waddir)/freedm.wad"                                   \
	      "$(target)$(docdir)/freedm/CREDITS"                               \
	      "$(target)$(docdir)/freedm/COPYING"                               \
	      "$(target)$(docdir)/freedm/NEWS.html"                             \
	      "$(target)$(docdir)/freedm/README.html"                           \
	      "$(target)$(docdir)/freedm/freedoom-manual.pdf"
	-rmdir -p "$(target)/share/applications"                    \
	      "$(target)/share/metainfo" "$(target)/share/icons"    \
	      "$(target)$(bindir)" "$(target)$(mandir)/man6"        \
	      "$(target)$(waddir)" "$(target)$(docdir)/freedm"

uninstall-freedoom:
	$(RM)                                                                   \
	      "$(target)/share/applications/io.github.freedoom.Phase1.desktop"  \
	      "$(target)/share/applications/io.github.freedoom.Phase2.desktop"  \
	      "$(target)/share/metainfo/io.github.freedoom.Phase1.metainfo.xml" \
	      "$(target)/share/metainfo/io.github.freedoom.Phase2.metainfo.xml" \
	      "$(target)/share/icons/io.github.freedoom.Phase1.png"             \
	      "$(target)/share/icons/io.github.freedoom.Phase2.png"             \
	      "$(target)$(bindir)/freedoom1"                                    \
	      "$(target)$(bindir)/freedoom2"                                    \
	      "$(target)$(mandir)/man6/freedoom1.6"                             \
	      "$(target)$(mandir)/man6/freedoom2.6"                             \
	      "$(target)$(waddir)/freedoom1.wad"                                \
	      "$(target)$(waddir)/freedoom2.wad"                                \
	      "$(target)$(docdir)/freedoom/CREDITS"                             \
	      "$(target)$(docdir)/freedoom/COPYING"                             \
	      "$(target)$(docdir)/freedoom/NEWS.html"                           \
	      "$(target)$(docdir)/freedoom/README.html"                         \
	      "$(target)$(docdir)/freedoom/freedoom-manual.pdf"
	-rmdir -p "$(target)/share/applications"                    \
	      "$(target)/share/metainfo" "$(target)/share/icons"    \
	      "$(target)$(bindir)" "$(target)$(mandir)/man6"        \
	      "$(target)$(waddir)" "$(target)$(docdir)/freedoom"

install: install-freedm install-freedoom

uninstall: uninstall-freedm uninstall-freedoom

snap: io.github.freedoom.Phase2.png
	cp ./dist/io.github.freedoom.Phase2.png snap/gui/io.github.freedoom.png
	snapcraft
