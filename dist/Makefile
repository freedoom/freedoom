man-%: freedoom.adoc
	sed -e s/freedoom/$*/ freedoom.adoc > $*.adoc
	a2x -f manpage $*.adoc

icon-freedm:
	convert -resize 64x64 ../graphics/captainw/freedm_title2.png \
	    freedm.png

icon-freedoom1:
	convert -trim +repage -extent 48x48 -gravity center \
	    -transparent \#00ffff -background \#00ffff \
	    ../sprites/playa2a8.gif freedoom1.png

icon-freedoom2:
	convert -trim +repage -extent 64x64 -gravity center \
	    -transparent \#00ffff -background \#00ffff \
	    ../sprites/heada1.gif freedoom2.png

clean:
	rm -f *.6 *.png freedm.adoc freedoom1.adoc freedoom2.adoc
