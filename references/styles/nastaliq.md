# Nastaliq — خط النستعليق

Alternate names: Nasta’liq, Nastaleeq, Persian.

## Background and visual features

A Persianate tradition especially associated with poetry and later Urdu typography. Suspended diagonal groups and descending words.

## Proportions, joining and composition

Proportions depend on pen width, school and period. This reference does not prescribe a universal dot-count formula. Arabic joining classes remain meaningful; a font cannot reproduce every historical alternate or custom overlap. The implementation uses the font’s OpenType substitutions and positioning, with Pango shaping and bidirectional paragraph layout.

## Uses and readability

Poetry and short display. Deep descenders need extra vertical room.

## Fonts, licensing and rendering

Bundled family: Noto Nastaliq Urdu Regular. See [font licenses](../../FONT_LICENSES.md) for exact versions, hashes and OFL embedding permissions. Output is font-based typography, not expert-certified classical calligraphy.

## Frequent errors

Do not infer authenticity from a style name, distort letters to fit a canvas, reverse Unicode, or insert ornamental marks into the linguistic text. Deep descenders need extra vertical room.

## Examples and references

Run `arabic-calligraphy render --style nastaliq --text "العلم نور" --output sample.svg`. Inspect marks, margins and reading order.

Source: https://www.iranicaonline.org/articles/calligraphy/calligraphy-ii-scripts/

Research status: introductory. These introductory notes are not a complete paleographic manual. Expert review and detailed school-specific measurements remain pending.
