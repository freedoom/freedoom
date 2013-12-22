COLORMAPS = colormap.lmp                                     \
            bloodmap.lmp bluemap.lmp lavamap.lmp nukemap.lmp \
	    fogmap.lmp mfademap.lmp

all: playpal.lmp $(COLORMAPS)

playpal.lmp: playpal-base.lmp playpal.py
	./playpal.py playpal-base.lmp > playpal.lmp

colormap.lmp: playpal.lmp colormap.py
	./colormap.py playpal.lmp > colormap.lmp

# Blue colormap applies a full blue tint. The brightness here is
# adjusted slightly because the default is too dark.

bluemap.lmp: playpal.lmp colormap.py
	./colormap.py --tint_color='#0000ff' --tint_pct=100 \
	              --tint_bright=0.6 playpal.lmp > bluemap.lmp

# "Fog" effect maps that darken to a color other than black:

fogmap.lmp: playpal.lmp colormap.py
	./colormap.py --dark_color='#505050' playpal.lmp > fogmap.lmp

mfademap.lmp: playpal.lmp colormap.py
	./colormap.py --dark_color='#2b230f' playpal.lmp > mfademap.lmp

# "Liquid" colormaps that apply a tint. With a liquid effect we also
# usually want to use --dark_color as well, because we want to darken
# to something like the liquid color instead of black.

bloodmap.lmp: playpal.lmp colormap.py
	./colormap.py --tint_color='#ff0000' --dark_color='#500000' \
	              --tint_pct=100 playpal.lmp > bloodmap.lmp

# TODO: The current lava effect is just very bright orange. Before the
# change to programatically-generated lavamap we had a better effect.
lavamap.lmp: playpal.lmp colormap.py
	./colormap.py --tint_color='#ff6000' --tint_pct=80 \
	              --tint_bright=0.8 --dark_color='#ff6000' \
		      playpal.lmp > lavamap.lmp

nukemap.lmp: playpal.lmp colormap.py
	./colormap.py --tint_color='#00ff00' --tint_pct=70 \
	              --dark_color='#005000' playpal.lmp > nukemap.lmp

clean:
	rm -f playpal.lmp $(COLORMAPS)

.PHONY: clean

