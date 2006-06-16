
WADS=wads
CPP=/usr/bin/cpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-fullsnd -rate accept -rgb 0 255 255
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

OBJS = \
	$(WADS)/freedoom.wad          \
	$(WADS)/freedoom_graphics.wad \
	$(WADS)/freedoom_levels.wad   \
	$(WADS)/freedoom_sprites.wad  \
	$(WADS)/freedoom_sounds.wad   \
	$(WADS)/freedoom_textures.wad \
	$(WADS)/doom1.wad	          \
	$(WADS)/doom2.wad             \
	$(WADS)/freedm.wad

# disable this for now
#	$(WADS)/freedoom_hires.zip

all : $(OBJS)

subdirs:
	make -C graphics/titlepic
	make -C lumps

# this is a useless dependency to force builds

force:

# build texture1.txt for different builds

textures/doom2/texture1.txt: textures/combined.txt
	$(CPP) -DDOOM1 -DDOOM2 < $< > $@
textures/doom/texture1.txt: textures/combined.txt
	$(CPP) -DDOOM1 < $< > $@
textures/freedm/texture1.txt: textures/combined.txt
	$(CPP) -DFREEDM < $< > $@
textures/shareware/texture1.txt: textures/combined.txt
	$(CPP) -DSHAREWARE < $< > $@

textures/%/pnames.txt: textures/%/texture1.txt
	./extract-pnames.pl < $< > $@

# update wadinfo.txt

wadinfo.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | ./wadinfo-builder.pl > $@
wadinfo_sw.txt: buildcfg.txt force textures/shareware/pnames.txt
	$(CPP) -P -DSHAREWARE < $< | ./wadinfo-builder.pl -dummy > $@
wadinfo_iwad.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | ./wadinfo-builder.pl -dummy > $@
wadinfo_freedm.txt : buildcfg.txt force textures/freedm/pnames.txt
	$(CPP) -P -DFREEDM < $< | ./wadinfo-builder.pl -dummy > $@

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
# graphics wad

$(WADS)/freedoom_graphics.wad : wadinfo.txt subdirs force 
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -graphics -build wadinfo.txt $@

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
	./makepkgs $(OBJS)

clean:
	rm -f	deutex.log $(OBJS) \
		./wadinfo.txt ./wadinfo_sw.txt \
		./wadinfo_freedm.txt ./wadinfo_iwad.txt
	make -C lumps clean
	make -C graphics/titlepic clean
