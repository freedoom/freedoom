man-%: freedoom.adoc
	sed -e s/freedoom/$*/ freedoom.adoc > $*.adoc
	a2x -f manpage $*.adoc

icon-freedm:
	convert -trim +repage -extent 32x32 -gravity center \
	    -transparent \#00ffff -background \#00ffff \
	    ../graphics/stfkill3.gif freedm.png

icon-freedoom1:
	convert -trim +repage -extent 48x48 -gravity center \
	    -transparent \#00ffff -background \#00ffff \
	    ../sprites/playa2a8.gif freedoom1.png

icon-freedoom2:
	convert -trim +repage -extent 64x64 -gravity center \
	    -transparent \#00ffff -background \#00ffff \
	    ../sprites/heada1.gif freedoom2.png
