
CPP=../../scripts/simplecpp

all: phase1/texture1.lmp phase2/texture1.lmp freedm/texture1.lmp

phase1/texture1.lmp:
	$(CPP) -DDOOM1 -DULTDOOM < textures.cfg |                \
	./build-textures -compat_texture1=doom1/texture1.txt     \
	                 -compat_texture2=doom1/texture2.txt     \
			 -compat_pnames=doom1/pnames.txt         \
			 -output_texture1=phase1/texture1.lmp    \
			 -output_texture2=phase1/texture2.lmp    \
			 -output_pnames=phase1/pnames.lmp        \
			 -output_pnames_txt=phase1/pnames.txt

phase2/texture1.lmp:
	$(CPP) -DDOOM1 -DDOOM2 < textures.cfg |                  \
	./build-textures -compat_texture1=doom2/texture1.txt     \
			 -compat_pnames=doom2/pnames.txt         \
			 -output_texture1=phase2/texture1.lmp    \
			 -output_pnames=phase2/pnames.lmp        \
			 -output_pnames_txt=phase2/pnames.txt

freedm/texture1.lmp:
	$(CPP) -DDOOM1 -DDOOM2 -DFREEDM < textures.cfg |         \
	./build-textures -compat_texture1=doom2/texture1.txt     \
			 -compat_pnames=doom2/pnames.txt         \
			 -output_texture1=freedm/texture1.lmp    \
			 -output_pnames=freedm/pnames.lmp        \
			 -output_pnames_txt=freedm/pnames.txt


clean:
	rm -f phase1/texture1.lmp phase1/texture2.lmp phase1/pnames.lmp \
	      phase1/pnames.txt                                         \
	      phase2/texture1.lmp phase2/pnames.lmp   phase2/pnames.txt \
	      freedm/texture1.lmp freedm/pnames.lmp   freedm/pnames.txt

