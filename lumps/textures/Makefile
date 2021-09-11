
CPP=../../scripts/simplecpp

all: phase1/texture1.lmp phase2/texture1.lmp freedm/texture1.lmp

phase1/texture1.lmp: textures.cfg
	@mkdir -p phase1
	$(CPP) -DDOOM1_VERSIONS < textures.cfg |                 \
	./build-textures -compat_texture1=doom1/texture1.txt     \
	                 -compat_texture2=doom1/texture2.txt     \
	                 -compat_pnames=doom1/pnames.txt         \
	                 -output_texture1=phase1/texture1.lmp    \
	                 -output_texture2=phase1/texture2.lmp    \
	                 -output_pnames=phase1/pnames.lmp        \
	                 -output_pnames_txt=phase1/pnames.txt    \
	                 -sprites_dir=../../sprites
	cp phase1/texture1.lmp ../fd1txtr1.lmp
	cp phase1/texture2.lmp ../fd1txtr2.lmp
	cp phase1/pnames.lmp   ../fd1pname.lmp

phase2/texture1.lmp: textures.cfg
	@mkdir -p phase2
	$(CPP) < textures.cfg |                                  \
	./build-textures -compat_texture1=doom2/texture1.txt     \
	                 -compat_pnames=doom2/pnames.txt         \
	                 -output_texture1=phase2/texture1.lmp    \
	                 -output_pnames=phase2/pnames.lmp        \
	                 -output_pnames_txt=phase2/pnames.txt    \
	                 -sprites_dir=../../sprites
	cp phase2/texture1.lmp ../fd2txtr1.lmp
	cp phase2/pnames.lmp   ../fd2pname.lmp

freedm/texture1.lmp: textures.cfg
	@mkdir -p freedm
	$(CPP) -DFREEDM < textures.cfg |                         \
	./build-textures -compat_texture1=doom2/texture1.txt     \
	                 -compat_pnames=doom2/pnames.txt         \
	                 -output_texture1=freedm/texture1.lmp    \
	                 -output_pnames=freedm/pnames.lmp        \
	                 -output_pnames_txt=freedm/pnames.txt    \
	                 -sprites_dir=../../sprites
	cp freedm/texture1.lmp ../fdmtxtr1.lmp
	cp freedm/pnames.lmp   ../fdmpname.lmp

clean:
	$(RM) phase1/texture1.lmp phase2/texture1.lmp freedm/texture1.lmp \
	      phase1/texture2.lmp                                         \
	      phase1/pnames.lmp   phase2/pnames.lmp   freedm/pnames.lmp   \
	      phase1/pnames.txt   phase2/pnames.txt   freedm/pnames.txt
	$(RM) ../fd1txtr1.lmp ../fd1txtr2.lmp ../fd1pname.lmp \
	      ../fd2txtr1.lmp ../fd2pname.lmp                 \
	      ../fdmtxtr1.lmp ../fdmpname.lmp
	-rmdir phase1 phase2 freedm
