PLAYPAL = ../playpal/playpal-base.lmp

COLORMAPS = colormap.lmp

all: $(COLORMAPS)
	cp $(COLORMAPS) ../

colormap.lmp: $(PLAYPAL) colormap
	./colormap $(PLAYPAL) > colormap.lmp

clean:
	$(RM) $(COLORMAPS) ../$(COLORMAPS)

.PHONY: clean
