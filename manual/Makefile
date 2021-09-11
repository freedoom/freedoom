all: freedoom-manual.pdf

freedoom-manual.pdf: manual.adoc
	-asciidoctor-pdf -a toc manual.adoc -o $@

clean:
	$(RM) freedoom-manual.pdf
