ASCIIDOCTOR_FLAGS = -a pdf-page-size=A5
all: freedoom-manual.pdf freedoom-manual-es.pdf freedoom-manual-fr.pdf

freedoom-manual.pdf: manual.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual.adoc -o $@

freedoom-manual-es.pdf: manual-es.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual-es.adoc -o $@

freedoom-manual-fr.pdf: manual-fr.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) manual-fr.adoc -o $@

clean:
	$(RM) freedoom-manual.pdf freedoom-manual-es.pdf freedoom-manual-fr.pdf
