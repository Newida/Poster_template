THEME ?= lamarr-classic
AVAILABLE_THEMES := lamarr-classic japanese-garden space
THEME_TARGETS := $(addprefix build-theme-,$(AVAILABLE_THEMES))
BUILD_DIR := build/$(THEME)
OUTPUT_DIR := output/pdf
THEME_PDF := $(OUTPUT_DIR)/poster-$(THEME).pdf
THEME_ASSETS :=
GARDEN_LOGOS := $(addprefix themes/japanese-garden/assets/logos/,lamarr.pdf tu-dortmund.pdf fraunhofer-iais.pdf fraunhofer-iml.pdf uni-bonn.pdf nrw.pdf bftr.pdf)

ifeq ($(THEME),japanese-garden)
THEME_ASSETS += $(GARDEN_LOGOS)
endif

ifeq ($(THEME),space)
THEME_ASSETS += themes/space/assets/inference_tree.pdf
endif

.PHONY: main theme themes clean FORCE $(THEME_TARGETS)

# `make` retains the historical poster.pdf output while also storing the
# named build under output/pdf/.
main: theme
	cp '$(THEME_PDF)' poster.pdf

theme: $(THEME_PDF)

themes: $(THEME_TARGETS)

$(THEME_TARGETS):
	$(MAKE) THEME=$(@:build-theme-%=%) theme

$(THEME_PDF): $(THEME_ASSETS) FORCE
	test -f 'themes/$(THEME)/theme.tex'
	mkdir -p '$(BUILD_DIR)' '$(OUTPUT_DIR)'
	latexmk -g -pdf \
		-outdir='$(BUILD_DIR)' \
		-jobname='poster-$(THEME)' \
		-usepretex='\def\PosterTheme{$(THEME)}' \
		-pdflatex='pdflatex -interaction=nonstopmode -halt-on-error %O %P %S' \
		poster.tex
	cp '$(BUILD_DIR)/poster-$(THEME).pdf' '$@'

$(GARDEN_LOGOS) &: scripts/build_garden_logos.py $(wildcard logos/*.png logos/*.svg logos/print-safe-light/*.png)
	python3 scripts/build_garden_logos.py

themes/space/assets/inference_tree.pdf: themes/space/assets/inference_tree.tex
	mkdir -p 'themes/space/assets'
	latexmk -pdf \
		-outdir='themes/space/assets' \
		-pdflatex='pdflatex -interaction=nonstopmode -halt-on-error %O %S' \
		'$<'
	latexmk -c -outdir='themes/space/assets' '$<'

clean:
	find build -depth -delete 2>/dev/null || true
	find output/pdf -maxdepth 1 -type f -name 'poster-*.pdf' -delete 2>/dev/null || true

FORCE:
