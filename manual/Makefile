# Generate the Freedoom manual PDF files based on ADOC files. Each translation
# has a two character code. Adding a new translation does not require any
# makefile changes, but it would be nice to keep the following table up to date:
#
# Two Character Code    Language
# ------------------    --------
#                 en    English
#                 es    Spanish
#                 fr    French

ASCIIDOCTOR_FLAGS = -a pdf-page-size=A5
MANUAL_ADOC_FILES=$(wildcard freedoom-manual-??.adoc)
MANUAL_PDF_FILES=$(subst .adoc,.pdf,$(MANUAL_ADOC_FILES))
PRINT_PDF_FILES=$(subst .adoc,-print.pdf,$(MANUAL_ADOC_FILES))
COVER_PDF_FILES=cover-en.pdf cover-es.pdf cover-fr.pdf
COVER_SVG_FILES=$(patsubst %.pdf,cover/%.svg,$(COVER_PDF_FILES))

all: $(MANUAL_PDF_FILES)

# `make print` builds all the PDFs for printed versions of the manuals.
print: covers $(PRINT_PDF_FILES)

# We only build the cover PDFs if the user explicitly runs `make covers`;
# this is because it requires Inkscape and we don't want it as a build
# dependency. Most users won't ever need these, we only use them when we're
# uploading the PDF files to print physical manuals.
covers: $(COVER_PDF_FILES)

freedoom-manual-%.pdf: freedoom-manual-%.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) $< -o $@

freedoom-manual-%-print.pdf: freedoom-manual-%.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) -a media=print $< -o $@

cover/cover-%.svg: cover/cover-%.sed cover/template.svg
	sed -f $< < cover/template.svg > $@

cover-%.pdf: cover/cover-%.svg cover/serpentipede.png cover/minigunner.png
	inkscape -o $@ $<

clean:
	$(RM) $(MANUAL_PDF_FILES) $(COVER_PDF_FILES) $(COVER_SVG_FILES) \
	      $(PRINT_PDF_FILES)

# Inkscape can't process files in parallel, it has to be sequential:
.NOTPARALLEL: covers
