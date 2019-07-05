all: man-freedm man-freedoom1 man-freedoom2 \
     icon-freedm icon-freedoom1 icon-freedoom2

man-%: freedoom.adoc
	sed -e s/freedoom/$*/ freedoom.adoc > $*.adoc
	a2x -f manpage $*.adoc

icon-freedm:
	./pillow-resize ../graphics/titlepic/freedm_title2.png freedm.png 64 64

icon-freedoom1:
	./pillow-compose ../sprites/playa2a8.png freedoom1.png 64 64

icon-freedoom2:
	./pillow-compose ../sprites/heada1.png freedoom2.png 64 64

clean:
	rm -f *.6 *.png freedm.adoc freedoom1.adoc freedoom2.adoc
