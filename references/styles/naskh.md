# Naskh — خط النسخ

Alternate names: Nesih, Naskhi.

## Background and visual features

A proportional book hand used widely in Arabic manuscript and modern text typography. Rounded forms and a relatively steady baseline.

## Proportions, joining and composition

Proportions depend on pen width, school and period. This reference does not prescribe a universal dot-count formula. Arabic joining classes remain meaningful; a font cannot reproduce every historical alternate or custom overlap. The implementation uses the font’s OpenType substitutions and positioning, with Pango shaping and bidirectional paragraph layout.

## Uses and readability

Body text, reports, letters. Dense marks require generous line spacing.

## Fonts, licensing and rendering

Bundled family: Noto Naskh Arabic Regular. See [font licenses](../../FONT_LICENSES.md) for exact versions, hashes and OFL embedding permissions. Output is font-based typography, not expert-certified classical calligraphy.

## Frequent errors

Do not infer authenticity from a style name, distort letters to fit a canvas, reverse Unicode, or insert ornamental marks into the linguistic text. Dense marks require generous line spacing.

## Examples and references

Run `arabic-calligraphy render --style naskh --text "العلم نور" --output sample.svg`. Inspect marks, margins and reading order.

Source: https://www.iranicaonline.org/articles/calligraphy/calligraphy-ii-scripts/

Research status: introductory. These introductory notes are not a complete paleographic manual. Expert review and detailed school-specific measurements remain pending.
