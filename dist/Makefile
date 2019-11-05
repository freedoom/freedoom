ASCIIDOC_MAN=a2x -f manpage
.SUFFIXES: .adoc .6

all: freedm.6 freedoom1.6 freedoom2.6 io.github.freedoom.FreeDM.png \
     io.github.freedoom.Phase1.png io.github.freedoom.Phase2.png

%.6: freedoom.adoc
	sed -e s/freedoom/$*/ $< > $*.adoc
	$(ASCIIDOC_MAN) $*.adoc

io.github.freedoom.FreeDM.png: ../graphics/titlepic/freedm_title2.png
	./pillow-resize $< $@ 64 64

io.github.freedoom.Phase1.png: ../sprites/playa2a8.png
	./pillow-compose $< $@ 64 64

io.github.freedoom.Phase2.png: ../sprites/heada1.png
	./pillow-compose $< $@ 64 64

clean:
	$(RM) *.6 *.png freedm.adoc freedoom1.adoc freedoom2.adoc
