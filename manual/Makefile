ASCIIDOCTOR_FLAGS = -a toc -a pdf-page-size=A5
all: freedoom-manual.pdf

freedoom-manual.pdf: manual.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual.adoc -o $@

clean:
	$(RM) freedoom-manual.pdf
