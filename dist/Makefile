man-%: freedoom.adoc
	sed -e s/freedoom/$*/ freedoom.adoc > $*.adoc
	a2x -f manpage $*.adoc

icon-freedm:
	convert -resize 64x64 ../graphics/captainw/freedm_title2.png \
	    freedm.png

icon-freedoom1:
	convert -resize 64x64 ../graphics/dist/phase1.png \
	    freedoom1.png

icon-freedoom2:
	convert -resize 64x64 ../graphics/dist/phase2.png \
	    freedoom2.png

clean:
	rm -f *.6 *.png freedm.adoc freedoom1.adoc freedoom2.adoc
