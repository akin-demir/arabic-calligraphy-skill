# Thuluth — خط الثلث

Alternate names: Sülüs, Sulus. Thuluth is a proportional cursive of the six pens, used in manuscript display and monumental lettering. Tall uprights, broad curves and carefully placed overlaps distinguish historical compositions. Proportions and alternates vary by school and period.

## Implemented typography

The unreleased `thuluth` workflow uses Mohammed Isam's **LaylaThuluth Regular 2.0**, unchanged under SIL OFL 1.1. Pango/HarfBuzz applies the font's contextual GSUB substitutions. PNG, outlined SVG and embedded-font PDF exports are implemented for **unvocalized text**:

```bash
arabic-calligraphy render --text "العلم نور" --style thuluth --output thuluth.svg
arabic-calligraphy poster --text "الخط العربي" --style thuluth --output poster.png
```

Use it for short headings and display lettering; use Naskh for readable body text. Never reverse strings, normalize marks without authorization, stretch letterforms or silently select another script.

## Positioning and PDF limits

This font has no GPOS table. Combining marks/harakat are explicitly refused rather than rendered with unverified positioning. Its original OS/2 fsType is 8 (editable embedding), which permits the implemented PDF workflow. That differs from Layla Diwani's fsType=2 restriction; Diwani PDF remains refused. The original font bytes and flags are retained. Generic Arabic PDF extraction/search/copy remains reader-dependent under PDF-001, even when the semantic source mapping and embedded font pass tests.

## Authenticity and composition

Classification: **Approximate font-based typography**. No independent expert authenticity review has occurred. The renderer lays out baseline typography; it does not reproduce historical pen proportions, free positioning, stacked compositions, artistic alternate selection or the hand-composed Thuluth specimen by ‘Ala’ al-Din Tabrizi. Do not claim that a font alone recreates such a manuscript.

## License and provenance

The font is part of the same Layla 2.0 collection already bundled for Diwani. Shared Layla-OFL.txt, Layla-Authors, Layla-FONTLOG.txt and Layla-SOURCE.md retain the license, reserved names and original attribution, including the Latin glyph credit. The mirror is pinned to NazirNayal8/nazirnayal.github.io commit d00ad06f30de6557a61bfe1e9bcdd4873eb4f7c7 and identifies ALT Linux fonts-ttf-layla 2.0-alt1_2. Runtime verifies the exact SHA-256 in data/fonts.json before registration.

Sources: https://fontlibrary.org/en/font/layla-thuluth ; https://fedoraproject.org/wiki/I18N/Fonts/Audit ; https://www.iranicaonline.org/articles/calligraphy/calligraphy-ii-scripts/ .

Historical visual reference: https://www.reed.edu/persian-calligraphy/en/ala-al-din-tabrizi/1/index.html . This reference is not presented as generated output or bundled in the gallery.
