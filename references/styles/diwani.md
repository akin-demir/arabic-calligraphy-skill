# Diwani — الخط الديواني

Alternate names: Divani. An Ottoman chancery tradition with rounded, sweeping forms and compact connections. This implementation is approximate font-based lettering, not a manually composed Diwani or Diwani Jali emblem.

## Implemented workflow

RC2 bundles Mohammed Isam's LaylaDiwani Regular, version 2.0, unchanged, under SIL OFL 1.1. It supports unvocalized Arabic display text and checked Latin/Common glyphs through Pango/HarfBuzz. Use it for short headings, names and wordmarks:

```bash
arabic-calligraphy render --text "العلم نور" --style diwani --size 1400x500 --font-size 180 --output diwani.svg
arabic-calligraphy poster --text "اللغة العربية" --style diwani --output poster.png
```

## Proportions, joining and composition

The font's GSUB table supplies contextual substitutions. Pen-width proportions vary by school; this package does not prescribe universal dot counts or interweave letters into a custom silhouette. Pango shapes logical Unicode; no manual reversal or reshaping is applied. Output is a baseline typesetting, not an Al Jazeera-like custom calligram.

## Supported formats and limitations

PNG and outlined SVG only. The original font has fsType=2 (restricted embedding), despite the accompanying OFL license permitting embedding generally. RC2 retains the original font bytes and refuses PDF use rather than silently overriding that flag. No GPOS table is present. Combining marks, including harakat, are refused rather than presented with unverified positioning. Do not use Diwani as a PDF document body style. Choose Naskh for vocalized text and documents.

The workflow does not implement Jali filling, special word overlaps or expert-certified classical composition. No human authenticity review has been obtained. Do not stretch letters, insert ornamental marks into linguistic text or silently replace this font with Naskh when installation fails.

## License and provenance

OFL allows redistribution; preserve the license, reserved font names and attribution, including the Latin glyph credit in the font metadata. The unmodified binary, exact SHA-256, license, author file and FONTLOG are bundled. The retrieved mirror is pinned to commit d00ad06f30de6557a61bfe1e9bcdd4873eb4f7c7; its SOURCE.md identifies ALT Linux fonts-ttf-layla 2.0-alt1_2. See FONT_LICENSES.md and package data/fonts.json.

Sources: https://fontlibrary.org/en/font/layla-diwani ; https://fedoraproject.org/wiki/I18N/Fonts/Audit ; https://www.iranicaonline.org/articles/calligraphy/calligraphy-ii-scripts/ .

Technical tests cover source integrity, coverage, actual exports, explicit refusals and a raster reference. They do not establish calligraphic authenticity or an artistic composition system.
