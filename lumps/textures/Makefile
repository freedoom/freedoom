
CPP=../../scripts/simplecpp
PHASE1_OUTPUTS = phase1/texture1.lmp phase1/texture2.lmp \
                 phase1/pnames.lmp
PHASE2_OUTPUTS = phase2/texture1.lmp phase2/pnames.lmp
FREEDM_OUTPUTS = freedm/texture1.lmp freedm/pnames.lmp

all: $(PHASE1_OUTPUTS) $(PHASE2_OUTPUTS) $(FREEDM_OUTPUTS)

$(PHASE1_OUTPUTS): textures.cfg
	$(CPP) -DDOOM1 -DULTDOOM < textures.cfg |                \
	./build-textures -compat_texture1=doom1/texture1.txt     \
	                 -compat_texture2=doom1/texture2.txt     \
			 -compat_pnames=doom1/pnames.txt         \
			 -output_texture1=phase1/texture1.lmp    \
			 -output_texture2=phase1/texture2.lmp    \
			 -output_pnames=phase1/pnames.lmp

$(PHASE2_OUTPUTS): textures.cfg
	$(CPP) -DDOOM1 -DDOOM2 < textures.cfg |                  \
	./build-textures -compat_texture1=doom2/texture1.txt     \
			 -compat_pnames=doom2/pnames.txt         \
			 -output_texture1=phase2/texture1.lmp    \
			 -output_pnames=phase2/pnames.lmp

$(FREEDM_OUTPUTS): textures.cfg
	$(CPP) -DDOOM1 -DDOOM2 -DFREEDM < textures.cfg |         \
	./build-textures -compat_texture1=doom2/texture1.txt     \
			 -compat_pnames=doom2/pnames.txt         \
			 -output_texture1=freedm/texture1.lmp    \
			 -output_pnames=freedm/pnames.lmp


clean:
	rm -f $(PHASE1_OUTPUTS) $(PHASE2_OUTPUTS) $(FREEDM_OUTPUTS)

