
CPP=/usr/bin/cpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-fullsnd -rate accept -rgb 0 255 255
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

OBJS = \
	wads/freedoom.wad          \
	wads/freedoom_graphics.wad \
	wads/freedoom_levels.wad   \
	wads/freedoom_sprites.wad  \
	wads/freedoom_sounds.wad   \
	wads/freedoom_textures.wad \
	wads/doom1.wad	          \
	wads/doom2.wad             \
	wads/freedm.wad

# disable this for now
#	wads/freedoom_hires.zip

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

wads:
	mkdir $@

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

wads/freedoom.wad: wadinfo.txt subdirs force wads
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -lumps -patch -flats -sounds -musics -graphics -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# freedm iwad

wads/freedm.wad: wadinfo_freedm.txt subdirs force wads
	ln -sf freedm/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_freedm.txt $@

#---------------------------------------------------------
# iwad

wads/doom2.wad: wadinfo_iwad.txt subdirs force wads
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_iwad.txt $@

#---------------------------------------------------------
# graphics wad

wads/freedoom_graphics.wad : wadinfo.txt subdirs force wads
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -graphics -build wadinfo.txt $@

#---------------------------------------------------------
# build levels wad

wads/freedoom_levels.wad : wadinfo.txt force wads
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -levels -build wadinfo.txt $@

#---------------------------------------------------------
# build texture wad

wads/freedoom_textures.wad : wadinfo.txt force wads
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -patch -flats -build wadinfo.txt $@

#---------------------------------------------------------
# build sprites wad

wads/freedoom_sprites.wad : wadinfo.txt force wads
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# build sounds wad

wads/freedoom_sounds.wad : wadinfo.txt force wads
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sounds -musics -build wadinfo.txt $@

#---------------------------------------------------------
# shareware iwad
# 
# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to the shareware wad

wads/doom1.wad : wadinfo_sw.txt force wads
	ln -sf shareware/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_sw.txt $@

dist : $(OBJS)
	./makepkgs $(OBJS)

clean:
	rm -f ./wadinfo.txt deutex.log $(OBJS)
	make -C lumps clean
