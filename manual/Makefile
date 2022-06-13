all: freedoom-manual.pdf freedoom-manual-es.pdf

freedoom-manual.pdf: manual.adoc
	-asciidoctor-pdf -a toc manual.adoc -o $@

freedoom-manual-es.pdf: manual-es.adoc
	-asciidoctor-pdf -a toc manual-es.adoc -o $@

clean:
	$(RM) freedoom-manual.pdf freedoom-manual-es.pdf
