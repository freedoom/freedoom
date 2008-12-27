# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008
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

WADS=wads
CPP=scripts/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-v0 -fullsnd -rate accept -rgb 0 255 255
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

OBJS = \
	$(WADS)/freedoom.wad          \
	$(WADS)/freedoom_levels.wad   \
	$(WADS)/freedoom_sprites.wad  \
	$(WADS)/freedoom_sounds.wad   \
	$(WADS)/freedoom_textures.wad \
	$(WADS)/doom1.wad	          \
	$(WADS)/doom2.wad             \
	$(WADS)/doom.wad	      \
	$(WADS)/freedm.wad

# disable this for now
#	$(WADS)/freedoom_hires.zip

all : $(OBJS)

subdirs:
	make -C graphics/titlepic
	make -C lumps
	make -C sprites/jond/placeholder

# this is a useless dependency to force builds

force:

# build texture1.txt for different builds

textures/doom2/texture1.txt: textures/combined.txt
	$(CPP) -DDOOM1 -DDOOM2 < $< > $@
textures/doom/texture1.txt: textures/combined.txt
	$(CPP) -DDOOM1 -DULTDOOM < $< > $@
textures/freedm/texture1.txt: textures/combined.txt
	$(CPP) -DFREEDM < $< > $@
textures/shareware/texture1.txt: textures/combined.txt
	$(CPP) -DSHAREWARE < $< > $@

textures/shareware/pnames.txt: textures/shareware/texture1.txt
	scripts/extract-pnames.py < $< > $@
textures/doom/pnames.txt: textures/doom/texture1.txt
	scripts/extract-pnames.py -a > $@
textures/doom2/pnames.txt: textures/doom2/texture1.txt 
	scripts/extract-pnames.py -a > $@
textures/freedm/pnames.txt: textures/freedm/texture1.txt
	scripts/extract-pnames.py -a > $@

# update wadinfo.txt

wadinfo.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | scripts/wadinfo-builder.py > $@
wadinfo_sw.txt: buildcfg.txt force textures/shareware/pnames.txt
	$(CPP) -P -DSHAREWARE < $< | scripts/wadinfo-builder.py -dummy > $@
wadinfo_iwad.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | scripts/wadinfo-builder.py -dummy > $@
wadinfo_ult.txt: buildcfg.txt force textures/doom/pnames.txt
	$(CPP) -P -DDOOM1 -DULTDOOM < $< | scripts/wadinfo-builder.py -dummy > $@
wadinfo_freedm.txt : buildcfg.txt force textures/freedm/pnames.txt
	$(CPP) -P -DFREEDM < $< | scripts/wadinfo-builder.py -dummy > $@

%.wad.gz: %.wad
	gzip < $< > $@
	chmod o-r $<
	md5sum $<.gz > $<.md5sum
	rm -f $<

#---------------------------------------------------------
# build wad

$(WADS)/freedoom.wad: wadinfo.txt subdirs force 
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -lumps -patch -flats -sounds -musics -graphics -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# freedm iwad

$(WADS)/freedm.wad: wadinfo_freedm.txt subdirs force 
	ln -sf freedm/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_freedm.txt $@

#---------------------------------------------------------
# iwad

$(WADS)/doom2.wad: wadinfo_iwad.txt subdirs force 
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_iwad.txt $@

#---------------------------------------------------------
# udoom iwad

$(WADS)/doom.wad: wadinfo_ult.txt subdirs force
	ln -sf doom/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_ult.txt $@

#---------------------------------------------------------
# build levels wad

$(WADS)/freedoom_levels.wad : wadinfo.txt force 
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -levels -build wadinfo.txt $@

#---------------------------------------------------------
# build texture wad

$(WADS)/freedoom_textures.wad : wadinfo.txt force 
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -patch -flats -build wadinfo.txt $@

#---------------------------------------------------------
# build sprites wad

$(WADS)/freedoom_sprites.wad : wadinfo.txt force 
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# build sounds wad

$(WADS)/freedoom_sounds.wad : wadinfo.txt force 
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sounds -musics -build wadinfo.txt $@

#---------------------------------------------------------
# shareware iwad
# 
# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to the shareware wad

$(WADS)/doom1.wad : wadinfo_sw.txt force
	ln -sf shareware/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_sw.txt $@

dist : $(OBJS)
	scripts/makepkgs $(OBJS)

clean:
	rm -f	deutex.log $(OBJS) \
		./wadinfo.txt ./wadinfo_sw.txt \
		./wadinfo_freedm.txt ./wadinfo_iwad.txt \
		./wadinfo_ult.txt \
		 ./lumps/freedoom.lmp \
		./textures/doom/pnames.txt \
		./textures/doom/texture1.txt \
		./textures/doom2/pnames.txt \
		./textures/doom2/texture1.txt \
		./textures/freedm/pnames.txt \
		./textures/freedm/texture1.txt \
		./textures/shareware/pnames.txt \
		./textures/shareware/texture1.txt \
		./textures/texture1.txt

	make -C lumps clean
	make -C graphics/titlepic clean
	make -C sprites/jond/placeholder clean
