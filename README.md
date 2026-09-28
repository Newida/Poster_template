# Themed LaTeX poster template

A reusable two-column `beamerposter` template with one content source and
swappable visual themes. The repository currently includes:

- `lamarr-classic` — the original dark-blue Lamarr layout
- `japanese-garden` — an ivory sumi-e layout adapted from
  `themes/Japanese_Garden.png`
- `space` — a midnight cosmic layout adapted from `themes/Space.png`

The classic and space themes use logos flattened against their solid bands.
The Japanese theme uses a vector Lamarr mark and cropped PDF partner logos
with clipping paths, allowing the paper artwork to show through without PNG
alpha soft masks. Its QR code appears above the evenly spaced footer logos.

## Build

Install a reasonably complete TeX Live distribution with `pdflatex`,
`latexmk`, `beamerposter`, TikZ/PGFPlots, Latin Modern, and TeX Gyre fonts.
The cropped Japanese logo PDFs are included. Rebuilding them after editing
the logo sources requires Python 3 with Pillow and MuPDF's `mutool` command.
Then run:

```bash
make                              # classic theme and poster.pdf
make THEME=japanese-garden theme  # Japanese theme only
make THEME=space theme            # space theme only
make themes                       # every bundled theme
make clean
```

Named PDFs are written to `output/pdf/`:

```text
output/pdf/poster-lamarr-classic.pdf
output/pdf/poster-japanese-garden.pdf
output/pdf/poster-space.pdf
```

The default theme and poster dimensions are set in `poster-config.tex`. A
Makefile `THEME=...` argument overrides the configured default for that build.

## Project structure

```text
poster.tex                 scientific content and title metadata
posterframework.sty        shared packages, geometry, and semantic components
poster-config.tex          default theme, page size, and scale
themes/<name>/theme.tex    colors, typography, background, header, and footer
themes/<name>/assets/      theme-specific artwork
logos/print-safe/          logos composited for the dark classic theme
logos/print-safe-light/    logos composited for light themes
scripts/build_garden_logos.py  convert Japanese logo assets to cropped PDFs
```

Content in `poster.tex` uses semantic colors and components supplied by the
framework, rather than styling individual themes directly. See
[`themes/README.md`](themes/README.md) for the theme contract and instructions
for adding another theme.

## Editing the poster

- Change the scientific content, figures, title, authors, and affiliations in
  `poster.tex`.
- Change the default theme or physical dimensions in `poster-config.tex`.
- Change only visual design in the selected theme's `theme.tex`.
- Keep raster background artwork at print resolution; the Japanese theme uses
  `background-print.jpg` for the PDF and keeps the smaller PNG as its editable
  source asset.
- The Japanese header mark and footer placement are in its `theme.tex`.
  Footer artwork lives in `themes/japanese-garden/assets/logos/`; equal
  spacing is measured between these cropped logo bounds, not padded canvases.

This project is based on the open-source
[Gemini](https://github.com/anishathalye/gemini) Beamer poster theme. Licensing
details are in [`LICENSE.md`](LICENSE.md).
