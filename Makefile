THEME ?= lamarr-classic
AVAILABLE_THEMES := lamarr-classic japanese-garden
THEME_TARGETS := $(addprefix build-theme-,$(AVAILABLE_THEMES))
BUILD_DIR := build/$(THEME)
OUTPUT_DIR := output/pdf
THEME_PDF := $(OUTPUT_DIR)/poster-$(THEME).pdf

.PHONY: main theme themes clean FORCE $(THEME_TARGETS)

# `make` retains the historical poster.pdf output while also storing the
# named build under output/pdf/.
main: theme
	cp '$(THEME_PDF)' poster.pdf

theme: $(THEME_PDF)

themes: $(THEME_TARGETS)

$(THEME_TARGETS):
	$(MAKE) THEME=$(@:build-theme-%=%) theme

$(THEME_PDF): FORCE
	test -f 'themes/$(THEME)/theme.tex'
	mkdir -p '$(BUILD_DIR)' '$(OUTPUT_DIR)'
	latexmk -g -pdf \
		-outdir='$(BUILD_DIR)' \
		-jobname='poster-$(THEME)' \
		-usepretex='\def\PosterTheme{$(THEME)}' \
		-pdflatex='pdflatex -interaction=nonstopmode -halt-on-error %O %P %S' \
		poster.tex
	cp '$(BUILD_DIR)/poster-$(THEME).pdf' '$@'

clean:
	find build -depth -delete 2>/dev/null || true
	find output/pdf -maxdepth 1 -type f -name 'poster-*.pdf' -delete 2>/dev/null || true

FORCE:
