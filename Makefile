
# date of the last release:

#LAST_RELEASE_DATE = "dec 25 2004"
LAST_RELEASE_DATE = "dec 25 2005"

WADS_DIR=/tmp/freedoom-wads

CPP=tools/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-fullsnd -rate accept -rgb 0 255 255
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

OBJS = \
	$(WADS_DIR)/freedoom.wad          \
	$(WADS_DIR)/freedoom_graphics.wad \
	$(WADS_DIR)/freedoom_levels.wad   \
	$(WADS_DIR)/freedoom_sprites.wad  \
	$(WADS_DIR)/freedoom_sounds.wad   \
	$(WADS_DIR)/freedoom_textures.wad \
	$(WADS_DIR)/doom1.wad	          \
	$(WADS_DIR)/doom2.wad

# disable this for now
#	$(WADS_DIR)/freedoom_hires.zip

usebuild :
	@echo please use the ./build wrapper script

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
textures/shareware/texture1.txt: textures/combined.txt
	$(CPP) -DSHAREWARE < $< > $@

textures/%/pnames.txt: textures/%/texture1.txt
	./extract-pnames.pl < $< > $@

$(WADS_DIR):
	mkdir $@

# update wadinfo.txt

wadinfo.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | ./wadinfo-builder.pl > $@
wadinfo_ulatest.txt: buildcfg.txt force textures/doom/pnames.txt
	$(CPP) -P -DDOOM1 < $< | ./wadinfo-builder.pl -since $(LAST_RELEASE_DATE) > $@
wadinfo_latest.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | ./wadinfo-builder.pl -since $(LAST_RELEASE_DATE) > $@
wadinfo_sw.txt: buildcfg.txt force textures/shareware/pnames.txt
	$(CPP) -P -DSHAREWARE < $< | ./wadinfo-builder.pl -dummy > $@
wadinfo_iwad.txt: buildcfg.txt force textures/doom2/pnames.txt
	$(CPP) -P -DDOOM2 < $< | ./wadinfo-builder.pl -dummy > $@

%.wad.gz: %.wad
	gzip < $< > $@
	chmod o-r $<
	md5sum $<.gz > $<.md5sum
	rm -f $<

#---------------------------------------------------------
# incremental wad

latest/ulatest.wad: wadinfo_ulatest.txt subdirs force
	# TODO: check this
	ln -sf doom/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_BASIC_ARGS) -doom bootstrap/ -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_ulatest.txt $@

latest/latest.wad: wadinfo_latest.txt subdirs force
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_BASIC_ARGS) -doom2 bootstrap/ -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_latest.txt $@

#---------------------------------------------------------
# build wad

$(WADS_DIR)/freedoom.wad: wadinfo.txt subdirs force $(WADS_DIR)
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -lumps -patch -flats -sounds -musics -graphics -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# iwad

$(WADS_DIR)/doom2.wad: wadinfo_iwad.txt subdirs force $(WADS_DIR)
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -textures -lumps -patch -flats -sounds -musics -graphics -sprites -levels -build wadinfo_iwad.txt $@

#---------------------------------------------------------
# graphics wad

$(WADS_DIR)/freedoom_graphics.wad : wadinfo.txt subdirs force $(WADS_DIR)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -graphics -build wadinfo.txt $@

#---------------------------------------------------------
# build levels wad

$(WADS_DIR)/freedoom_levels.wad : wadinfo.txt force $(WADS_DIR)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -levels -build wadinfo.txt $@

#---------------------------------------------------------
# build texture wad

$(WADS_DIR)/freedoom_textures.wad : wadinfo.txt force $(WADS_DIR)
	ln -sf doom2/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -textures -patch -flats -build wadinfo.txt $@

#---------------------------------------------------------
# build sprites wad

$(WADS_DIR)/freedoom_sprites.wad : wadinfo.txt force $(WADS_DIR)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sprites -build wadinfo.txt $@

#---------------------------------------------------------
# build sounds wad

$(WADS_DIR)/freedoom_sounds.wad : wadinfo.txt force $(WADS_DIR)
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -sounds -musics -build wadinfo.txt $@

#---------------------------------------------------------
# shareware iwad
# 
# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to the shareware wad

$(WADS_DIR)/doom1.wad : wadinfo_sw.txt force $(WADS_DIR)
	ln -sf shareware/texture1.txt textures/texture1.txt
	rm -f $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_sw.txt $@

#---------------------------------------------------------
# hires texture zip

HIRES_SRC=$(wildcard patches_hi/*.png) $(wildcard flats_hi/*.png)
HIRES_TGA=$(HIRES_SRC:%.png=.tga/%.tga)

.tga/%.tga : %.png
	pngtopnm < $< | ppmtotga > $@

$(WADS_DIR)/freedoom_hires.zip : $(HIRES_TGA) $(WADS_DIR)
	rm -f $(WADS_DIR)/freedoom_hires.zip
	zip -j $(WADS_DIR)/freedoom_hires.zip $(HIRES_TGA) > /dev/null

dist : $(OBJS)
	./makepkgs $(OBJS)


