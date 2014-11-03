# Copyright (c) 2001-2014
# Contributors to the Freedoom project.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the freedoom project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

VERSION=$(shell git describe 2>/dev/null || cat VERSION)
WADS=wads
CPP=scripts/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-v0 -fullsnd -rate accept -rgb 0 255 255
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

FREEDOOM1=$(WADS)/freedoom1.wad
FREEDOOM2=$(WADS)/freedoom2.wad
FREEDM=$(WADS)/freedm.wad

OBJS=$(FREEDM) $(FREEDOOM1) $(FREEDOOM2)

all: $(OBJS)

subdirs:
	$(MAKE) -C graphics/text
	$(MAKE) VERSION=$(VERSION) -C graphics/titlepic
	$(MAKE) -C lumps/cph/misc-lumps
	$(MAKE) -C lumps/genmidi
	$(MAKE) -C lumps/dmxgus
	$(MAKE) -C lumps/textures


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
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_phase1.txt $@

#---------------------------------------------------------
# phase 2 (doom2) iwad

$(FREEDOOM2): wadinfo_phase2.txt subdirs
	@mkdir -p $(WADS)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_phase2.txt $@

%.html: %.adoc
	asciidoc $<

doc: $(patsubst %.adoc,%.html,$(wildcard *.adoc))

DISTDOCS=COPYING CREDITS README.html

.PHONY: dist

# Due to convoluted reasons, the WADs must directly proceed the game name.
dist: $(OBJS) README.html
	VERSION=$(VERSION) scripts/makepkgs freedm $(FREEDM) $(DISTDOCS)
	VERSION=$(VERSION) scripts/makepkgs freedoom $(FREEDOOM1) $(FREEDOOM2) $(DISTDOCS)

json: $(OBJS)
ifndef JSON
	@echo "Define JSON as the file to output." >&2
	@exit 1
else
	JSON=$(JSON) VERSION=$(VERSION) scripts/makejson
endif

clean:
	rm -f	*.html deutex.log $(OBJS) \
		./wadinfo.txt ./wadinfo_phase1.txt \
		./wadinfo_phase2.txt ./wadinfo_freedm.txt \
		./lumps/freedoom.lmp \
		./lumps/freedm.lmp
	-rmdir $(WADS)

	$(MAKE) -C dist clean
	$(MAKE) -C graphics/text clean
	$(MAKE) -C graphics/titlepic clean
	$(MAKE) -C lumps/cph/misc-lumps clean
	$(MAKE) -C lumps/genmidi clean
	$(MAKE) -C lumps/dmxgus clean
	$(MAKE) -C lumps/textures clean

prefix?=/usr/local
bindir?=/bin
mandir?=/share/man
waddir?=/share/games/doom
target=$(DESTDIR)$(prefix)

%.6:
	$(MAKE) -C dist man-$*

%.png:
	$(MAKE) -C dist icon-$*

# This is bad because it assumes the IWADs will always be defined like
# this.  I just can't see another way to do it.  Fix later if possible.

install-%: $(WADS)/%.wad %.6 %.png
	install -d "$(target)$(bindir)"
	install -m 755 dist/freedoom "$(target)$(bindir)/$*"
	install -d "$(target)$(mandir)/man6"
	install -m 644 dist/$*.6 "$(target)$(mandir)/man6"
	install -d "$(target)$(waddir)"
	install -m 644 $(WADS)/$*.wad "$(target)$(waddir)"
	install -d "$(target)/share/applications"
	install -m 644 dist/$*.desktop "$(target)/share/applications"
	install -d "$(target)/share/appdata"
	install -m 644 dist/$*.appdata.xml "$(target)/share/appdata"
	install -d "$(target)/share/icons"
	install -m 644 dist/$*.png "$(target)/share/icons/$*.png"

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
