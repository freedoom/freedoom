ASCIIDOC_MAN=a2x -f manpage
.SUFFIXES: .adoc .6

all: freedm.6 freedoom1.6 freedoom2.6 freedm.png freedoom1.png freedoom2.png

%.6: freedoom.adoc
	sed -e s/freedoom/$*/ $< > $*.adoc
	$(ASCIIDOC_MAN) $*.adoc

freedm.png: ../graphics/titlepic/freedm_title2.png
	./pillow-resize $< $@ 64 64

freedoom1.png: ../sprites/playa2a8.png
	./pillow-compose $< $@ 64 64

freedoom2.png: ../sprites/heada1.png
	./pillow-compose $< $@ 64 64

clean:
	$(RM) *.6 *.png freedm.adoc freedoom1.adoc freedoom2.adoc
