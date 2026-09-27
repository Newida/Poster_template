.PHONY: main clean FORCE

main: poster.pdf

poster.pdf: FORCE
	latexmk -pdf -pdflatex='pdflatex -interaction=nonstopmode -halt-on-error %O %S' poster.tex

clean:
	latexmk -pdf -C
