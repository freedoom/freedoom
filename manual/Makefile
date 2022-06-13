ASCIIDOCTOR_FLAGS = -a toc -a pdf-page-size=A5
all: freedoom-manual.pdf freedoom-manual-es.pdf

freedoom-manual.pdf: manual.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual.adoc -o $@

freedoom-manual-es.pdf: manual-es.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual-es.adoc -o $@

clean:
	$(RM) freedoom-manual.pdf freedoom-manual-es.pdf
