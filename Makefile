# SPDX-License-Identifier: BSD-3-Clause

VERSION=$(shell git describe --abbrev=8 --dirty 2>/dev/null || echo v0.11.3)
WADS=wads
ASCIIDOC=asciidoc
ASCIIDOC_MAN=a2x -f manpage
CPP=scripts/simplecpp
DEUTEX=deutex
DEUTEX_BASIC_ARGS=-v0 -rate accept
DEUTEX_ARGS=$(DEUTEX_BASIC_ARGS) -doom2 bootstrap/

FREEDOOM1=$(WADS)/freedoom1.wad
FREEDOOM2=$(WADS)/freedoom2.wad
FREEDM=$(WADS)/freedm.wad

OBJS=$(FREEDM) $(FREEDOOM1) $(FREEDOOM2)

.PHONY: clean dist

all: $(OBJS)

subdirs:
	$(MAKE) -C lumps/dehacked # graphics/text depends on generated dehacked files
	$(MAKE) VERSION=$(VERSION) -C graphics/text
	$(MAKE) -C lumps/playpal
	$(MAKE) -C lumps/colormap
	$(MAKE) -C lumps/genmidi
	$(MAKE) -C lumps/dmxgus
	$(MAKE) -C lumps/textures
	$(MAKE) -C bootstrap


# this is a useless dependency to force builds

force:

lumps/freedoom.lmp lumps/freedm.lmp: force
	echo $(VERSION) > $@

# deutex doesnt allow redirects for the filenames in the texture
# entries, so we have to change the texture1 symlink to point
# to whichever wad we are working on

#---------------------------------------------------------
# freedm iwad

wadinfo_freedm.txt : buildcfg.txt subdirs lumps/freedoom.lmp lumps/freedm.lmp
	$(CPP) -P -DFREEDM < $< > $@

$(FREEDM): wadinfo_freedm.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_freedm.txt $@

#---------------------------------------------------------
# phase 1 (udoom) iwad

wadinfo_phase1.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DPHASE1 < $< > $@

$(FREEDOOM1): wadinfo_phase1.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase1.txt $@

#---------------------------------------------------------
# phase 2 (doom2) iwad

wadinfo_phase2.txt: buildcfg.txt subdirs lumps/freedoom.lmp
	$(CPP) -P -DPHASE2 < $< > $@

$(FREEDOOM2): wadinfo_phase2.txt subdirs
	@mkdir -p $(WADS)
	$(RM) $@
	$(DEUTEX) $(DEUTEX_ARGS) -iwad -build wadinfo_phase2.txt $@

%.html: %.adoc
	TZ=UTC $(ASCIIDOC) $<

manual/freedoom-manual.pdf: manual/manual.adoc
	$(MAKE) -C manual

COPYING.txt: COPYING.adoc
	unix2dos --add-bom --newfile $< $@

CREDITS.txt: CREDITS
	unix2dos --add-bom --newfile $< $@

HTMLDOCS=NEWS.html README.html
TEXTDOCS=COPYING.txt CREDITS.txt
DISTDOCS=$(HTMLDOCS) $(TEXTDOCS) manual/freedoom-manual.pdf

dist: $(OBJS) $(DISTDOCS)
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedm $(FREEDM) $(DISTDOCS)
	LC_ALL=C VERSION=$(VERSION) scripts/makepkgs freedoom $(FREEDOOM1) $(FREEDOOM2) $(DISTDOCS)

json: $(OBJS)
ifndef JSON
	@echo "Define JSON as the file to output." >&2
	@exit 1
else
	JSON=$(JSON) VERSION=$(VERSION) scripts/makejson
endif

doom.gpl: lumps/playpal/playpal-base.lmp
	$(MAKE) -C lumps/playpal $@
	mv lumps/playpal/$@ .

gimp-palette: doom.gpl

clean: wad-image-clean
	$(RM) *.html doom.gpl $(OBJS) \
	      ./COPYING.txt ./CREDITS.txt \
	      ./wadinfo_phase1.txt \
	      ./wadinfo_phase2.txt \
	      ./wadinfo_freedm.txt \
	      ./lumps/freedoom.lmp \
	      ./lumps/freedm.lmp
	-rmdir $(WADS)

	$(MAKE) -C bootstrap clean
	$(MAKE) -C dist clean
	$(MAKE) -C graphics/text clean
	$(MAKE) -C lumps/dehacked clean
	$(MAKE) -C lumps/playpal clean
	$(MAKE) -C lumps/colormap clean
	$(MAKE) -C lumps/genmidi clean
	$(MAKE) -C lumps/dmxgus clean
	$(MAKE) -C lumps/textures clean
	$(MAKE) -C manual clean

# Variables that are common to wad-image* targets.
WI_LEVELS := levels
WI_SCRIPTS := scripts
WI_PATH := $(shell command -v wad2image.py)
WI_HOME := $(if $(WAD2IMAGE_HOME),$(WAD2IMAGE_HOME),$(if $(WI_PATH),$(shell $(WI_PATH) \
    --get-top-dir),$(WI_SCRIPTS)/wad2image))
WI_IMAGES := wad-images
WI_WAD_SPATH := wads,{top-dir}/wads,.,/usr/share/doom,/usr/local/doom
WI_ALL_OPTIONS := $(WI_OPTIONS) $(if $(WI_BW), --colors-images bw,) \
    $(if $(WI_CMD), --show-cmd $(WI_CMD),) $(if $(WI_GIF), -d gif,) \
    $(if $(WI_IMAGES), --out-dir $(WI_IMAGES),) $(if $(WI_SHOW), -s,) \
    $(if $(WI_VERBOSE), -v,) $(if $(WI_WAD_SPATH), --wad-spath $(WI_WAD_SPATH),)
wad-image-common:
ifndef WI_IMAGES
	$(error WI_IMAGES must be defined)
endif
ifndef WI_LEVELS
	$(error WI_LEVELS must be defined)
endif
ifndef WI_SCRIPTS
	$(error WI_SCRIPTS must be defined)
endif
ifndef WI_HOME
	$(error WI_HOME must be defined)
endif

# Generating images for WADs in "levels" directory and show the result.
WI_LATEST := $(shell ls -1t $(WI_LEVELS)/*.wad | head -n 1)
WI_FILES := $(if $(WI_PATT), $(WI_LEVELS)/$(WI_PATT).wad, $(WI_LATEST))
wad-image: wad-image-common
	@echo "Generating images for WADs in \"$(WI_LEVELS)\"."
	$(WI_HOME)/bin/wad2image.py $(WI_ALL_OPTIONS) $(WI_FILES)

# Cleanup generated images. Structured this way for safety.
wad-image-clean: wad-image-common
	$(RM) $(WI_IMAGES)/*
	-rmdir $(WI_IMAGES)

# Diffing WADs in "levels" using git and show the diff."
wad-image-diff: wad-image-common
	@echo "Diffing WADs in \"$(WI_LEVELS)\" using git."
	$(WI_HOME)/integration/git-wad-diff.sh "$(WI_COMMIT)" "$(WI_LEVELS)" $(WI_ALL_OPTIONS)

# Help for wad2image.
wad-image-help: wad-image-common
	@echo "Help for wad-image* targets and WI_* variable which can be used to see"
	@echo "differences between WAD revisions, or to simply view WADs. The following targets"
	@echo "depend on wad2image being installed with bin/wad2image.py in it being in the"
	@echo "path, or alteratively wad2image being copied or symlinked to the \"$(WI_SCRIPTS)\""
	@echo "directory. Images are created in \"$(WI_IMAGES)\". Each variable's description"
	@echo "ends with \"Value:\" followed by that variable's current value. If no variables"
	@echo "have been specified on the make command line then the value shown is the"
	@echo "default value. Some variables are unset by default. wad2image can be downloaded"
	@echo "from http://selliott.org/utilities/wad2image."
	@echo ""
	@echo "  Targets:"
	@echo ""
	@echo "    wad-image       Generate generate images for WAD files that are in the"
	@echo "                    workspace."
	@echo "    wad-image-clean Remove \"$(WI_IMAGES)\" as well as all files in it."
	@echo "    wad-image-diff  Use git to generate diff image showing the differences"
	@echo "                    between two revisions of WAD files. By default the"
	@echo "                    difference is between latest HEAD and the workspace, but the"
	@echo "                    WI_COMMIT variable can be used to generate other diffs."
	@echo "    wad-image-help  This help message."
	@echo ""
	@echo "  Variables:"
	@echo ""
	@echo "    WI_BW           Make diff images black or white (high contrast) instead of"
	@echo "                    full color. This applies to wad-image-diff-only."
	@echo "                    Value: $(WI_BW)"
	@echo "    WI_CMD          Command used to display images. \"display\" is used if no"
	@echo "                    value is specified. \"animate\" works well for animated"
	@echo "                    GIFs. Value: $(WI_CMD)"
	@echo "    WI_COMMIT       When the wad-image-diff target is invoked this variable"
	@echo "                    specifies which revisions are compared. It's similar to"
	@echo "                    git's \"commit\" argument. Value: $(WI_COMMIT)"
	@echo "    WI_GIF          Create animated GIFs instead of color coded files for the"
	@echo "                    diff. Value: $(WI_GIF)"
	@echo "    WI_HOME         The location where wad2image is installed. By default PATH"
	@echo "                    is searched for \"wad2image.py\". If it's found the"
	@echo "                    enclosing installation directory is used. If it's not found"
	@echo "                    $(WI_SCRIPTS)/wad2image is used. Value: $(WI_HOME)"
	@echo "    WI_IMAGES       The output directory that will contain the images created."
	@echo "                    Value: $(WI_IMAGES)"
	@echo "    WI_LEVELS       Subdirectory with the level WADs. Value: $(WI_IMAGES)"
	@echo "    WI_OPTIONS      Additional command line options for wad2image."
	@echo "                    Value: $(WI_OPTIONS)"
	@echo "    WI_SHOW         If set then show the images after creating them."
	@echo "                    Value: $(WI_SHOW)"
	@echo "    WI_PATT         Files patterns that are applied to files in the"
	@echo "                    \"$(WI_LEVELS)\" directory without the \".wad\" suffix. For"
	@echo "                    example, \"map0*\" to get MAP01 - MAP09. This applies to"
	@echo "                    wad-image only. Value: $(WI_PATT)"
	@echo "    WI_VERBOSE      If set then make wad2image more verbose."
	@echo "                    Value: $(WI_VERBOSE)"
	@echo "    WI_WAD_SPATH    The search path for WADs where a fully qualified path was"
	@echo "                    not given. This is typically used for the IWAD. By default"
	@echo "                    \"wads\" is searched first, so it helps to complete a build"
	@echo "                    before generating images. Value: $(WI_WAD_SPATH)"
	@echo ""
	@echo "  Examples:"
	@echo ""
	@echo "    Verbosely create and display an image for the most recently modified WAD"
	@echo "    file in \"levels\":"
	@echo "      make wad-image WI_VERBOSE=t"
	@echo ""
	@echo "    Create and display the image for MAP05:"
	@echo "      make wad-image WI_PATT=map05"
	@echo ""
	@echo "    Verbosely create color coded diffs for changed files in the workspace:"
	@echo "      make wad-image-diff WI_VERBOSE=t"
	@echo ""
	@echo "    Same as above but Yadex style (example of WI_OPTIONS):"
	@echo "      make wad-image-diff WI_VERBOSE=t WI_OPTIONS=\"-c yadex\""
	@echo ""
	@echo "    Same as the above, but with high contrast black or white images, but"
	@echo "      without Yadex style:"
	@echo "      make wad-image-diff WI_VERBOSE=t WI_BW=t"
	@echo ""
	@echo "    Same as above, but use animated GIFs to illustrate the diff instead of"
	@echo "    colors. Also, once the animated GIFs are created they'll be shown with"
	@echo "    the \"animate\" command:"
	@echo "      make wad-image-diff WI_VERBOSE=t WI_GIF=t WI_SHOW=t WI_CMD=animate"
	@echo ""
	@echo "    Same as above, but illustrate the diff between two git revisions instead of"
	@echo "    the workspace:"
	@echo "      make wad-image-diff WI_VERBOSE=t WI_GIF=t WI_SHOW=t WI_CMD=animate \
WI_COMMIT=\"0c004ce~..0c004ce\""

# Test targets all of which are a dependency of "test".

# Test that WAD files have the expected map names.
test-map-names:
	scripts/fix-map-names -t levels

# Run all tests. Add test-* targets above, and then as a dependency here.
test: test-map-names
	@echo
	@echo "All tests passed."

# Non-test targets that run scripts in the "scripts" directory.

# Fix the map names.
fix-map-names:
	scripts/fix-map-names levels

%.6:
	$(MAKE) ASCIIDOC_MAN="$(ASCIIDOC_MAN)" -C dist $@

%.png:
	$(MAKE) -C dist $@

prefix?=/usr/local
bindir?=/bin
docdir?=/share/doc
mandir?=/share/man
waddir?=/share/games/doom
target=$(DESTDIR)$(prefix)

install_metadata_freedm:
	install -Dm 644 dist/io.github.freedoom.FreeDM.desktop -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.FreeDM.metainfo.xml -t "$(target)/share/metainfo"

install_metadata_freedoom1:
	install -Dm 644 dist/io.github.freedoom.Phase1.desktop -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.Phase1.metainfo.xml -t "$(target)/share/metainfo"

install_metadata_freedoom2:
	install -Dm 644 dist/io.github.freedoom.Phase2.desktop -t "$(target)/share/applications"
	install -Dm 644 dist/io.github.freedoom.Phase2.metainfo.xml -t "$(target)/share/metainfo"

uninstall_metadata_freedm:
	$(RM) "$(target)/share/applications/io.github.freedoom.FreeDM.desktop"
	$(RM) "$(target)/share/metainfo/io.github.freedoom.FreeDM.metainfo.xml"
	-rmdir -p "$(target)/share/applications"
	-rmdir -p "$(target)/share/metainfo"

uninstall_metadata_freedoom1:
	$(RM) "$(target)/share/applications/io.github.freedoom.Phase1.desktop"
	$(RM) "$(target)/share/metainfo/io.github.freedoom.Phase1.metainfo.xml"
	-rmdir -p "$(target)/share/applications"
	-rmdir -p "$(target)/share/metainfo"

uninstall_metadata_freedoom2:
	$(RM) "$(target)/share/applications/io.github.freedoom.Phase2.desktop"
	$(RM) "$(target)/share/metainfo/io.github.freedoom.Phase2.metainfo.xml"
	-rmdir -p "$(target)/share/applications"
	-rmdir -p "$(target)/share/metainfo"

install-%: $(WADS)/%.wad                          \
           $(HTMLDOCS) manual/freedoom-manual.pdf \
           %.6 %.png install_metadata_%
	install -Dm 755 dist/freedoom "$(target)$(bindir)/$*"
	install -Dm 644 dist/$*.6 -t "$(target)$(mandir)/man6"
	install -Dm 644 $(WADS)/$*.wad -t "$(target)$(waddir)"
	install -Dm 644 dist/$*.png -t "$(target)/share/icons"
	install -Dm 644 CREDITS NEWS.html README.html -t "$(target)$(docdir)/$*"
	install -Dm 644 COPYING.adoc "$(target)$(docdir)/$*/COPYING"
	-install -Dm 644 manual/freedoom-manual.pdf -t "$(target)$(docdir)/$*"

uninstall-%: uninstall_metadata_%
	$(RM) "$(target)$(bindir)/$*"
	$(RM) "$(target)$(mandir)/man6/$*.6"
	$(RM) "$(target)$(waddir)/$*.wad"
	$(RM) "$(target)/share/icons/$*.png"
	$(RM) "$(target)$(docdir)/$*/CREDITS" "$(target)$(docdir)/$*/COPYING"
	$(RM) "$(target)$(docdir)/$*/NEWS.html" "$(target)$(docdir)/$*/README.html"
	$(RM) "$(target)$(docdir)/$*/freedoom-manual.pdf"
	-rmdir -p "$(target)$(bindir)"
	-rmdir -p "$(target)$(mandir)/man6"
	-rmdir -p "$(target)$(waddir)"
	-rmdir -p "$(target)/share/icons"
	-rmdir -p "$(target)$(docdir)/$*"

install: install-freedm install-freedoom1 install-freedoom2

uninstall: uninstall-freedm uninstall-freedoom1 uninstall-freedoom2
