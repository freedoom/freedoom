PLAYPAL = ../playpal/playpal-base.lmp

COLORMAPS = colormap.lmp                                     \
            bloodmap.lmp bluemap.lmp lavamap.lmp nukemap.lmp \
	    fogmap.lmp mfademap.lmp

all: $(COLORMAPS)
	cp $(COLORMAPS) ../

colormap.lmp: $(PLAYPAL) colormap.py
	./colormap.py $(PLAYPAL) > colormap.lmp

# Blue colormap applies a full blue tint. The brightness here is
# adjusted slightly because the default is too dark.

bluemap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --tint_color='#0000ff' --tint_pct=100 \
	              --tint_bright=0.6 $(PLAYPAL) > bluemap.lmp

# "Fog" effect maps that darken to a color other than black:

fogmap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --dark_color='#505050' $(PLAYPAL) > fogmap.lmp

mfademap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --dark_color='#2b230f' $(PLAYPAL) > mfademap.lmp

# "Liquid" colormaps that apply a tint. With a liquid effect we also
# usually want to use --dark_color as well, because we want to darken
# to something like the liquid color instead of black.

bloodmap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --tint_color='#ff0000' --dark_color='#500000' \
	              --tint_pct=100 $(PLAYPAL) > bloodmap.lmp

# TODO: The current lava effect is just very bright orange. Before the
# change to programatically-generated lavamap we had a better effect.
lavamap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --tint_color='#ff6000' --tint_pct=80 \
	              --tint_bright=0.8 --dark_color='#ff6000' \
		      $(PLAYPAL) > lavamap.lmp

nukemap.lmp: $(PLAYPAL) colormap.py
	./colormap.py --tint_color='#00ff00' --tint_pct=70 \
	              --dark_color='#005000' $(PLAYPAL) > nukemap.lmp

clean:
	rm -f $(COLORMAPS)

.PHONY: clean

