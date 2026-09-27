# Poster themes

Select a theme through `poster-config.tex` or the Makefile:

```bash
make THEME=lamarr-classic
make THEME=japanese-garden
make themes
```

Every theme lives in `themes/<name>/theme.tex`. A theme may also contain an
`assets/` directory. Theme files configure semantic colors, typography,
backgrounds, Beamer block templates, the header and the footer. Scientific
content remains in `poster.tex`; a theme must not duplicate it.

To add a theme:

1. Copy an existing theme directory.
2. Rename the directory and update its `theme.tex`.
3. Build it with `make THEME=<name> theme`.
4. Add its name to `AVAILABLE_THEMES` in the Makefile only if it should be
   included by `make themes`.

Poster content should use the shared semantic colors (`DarkNavy`, `Aqua`,
`CrispWhite`, `SoftGray`, and `TakeawayAccent`) and the framework components
`posterfeatureblock`, `postertakeaways`, `statcallout`, and
`posteroptionalheading`. `PosterTitleBreakA` and `PosterTitleBreakB` are title
layout hooks: they are spaces by default, but a theme may redefine them as
line breaks. This keeps content portable between visual themes.

At minimum, a theme should set the semantic Beamer colors and provide headline
and footline templates. It may redefine the feature/takeaway hooks when those
sections need a treatment different from ordinary blocks. See the two bundled
themes for a minimal classic example and a fully custom example with a raster
background and bespoke section headings.
