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

all: $(MANUAL_PDF_FILES)

freedoom-manual-%.pdf: freedoom-manual-%.adoc
	-asciidoctor-pdf $(ASCIIDOCTOR_FLAGS) $< -o $@

clean:
	$(RM) $(MANUAL_PDF_FILES)
