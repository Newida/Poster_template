# Japanese garden logo assets

These PDFs paint only logo artwork, so the actual paper background remains
visible around and between the marks. There is no rectangular paper-color
backing and no alpha soft mask (`/SMask`) in any logo asset.

`lamarr.pdf` retains the paths from `logos/lamarr-logo-template.svg`, cropped
to the artwork and set in the theme's navy. The six partner logos retain their
existing RGB artwork and use geometric clipping paths derived from the
original PNG silhouettes. White details inside colored emblems are preserved;
wordmarks use the existing light-theme variants for contrast on paper.

Regenerate from the repository root with:

```bash
python3 scripts/build_garden_logos.py
```

Requires Pillow and MuPDF (`mutool`). The Makefile also regenerates these PDFs
when their source logos or converter change. Theme layout uses cropped bounds,
one vertical center, and identical flexible gaps for the six footer logos.
