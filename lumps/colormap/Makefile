PLAYPAL = ../playpal/playpal-base.lmp

COLORMAPS = colormap.lmp

all: $(COLORMAPS)
	cp $(COLORMAPS) ../

colormap.lmp: $(PLAYPAL) colormap.py
	./colormap.py $(PLAYPAL) > colormap.lmp

clean:
	rm -f $(COLORMAPS) ../$(COLORMAPS)

.PHONY: clean
