# Bundled fonts

Runtime assets live in src/arabic_calligraphy/data/fonts/ so wheels work offline. The source/version/hash manifest is src/arabic_calligraphy/data/fonts.json. Four unmodified Noto families, Layla Diwani and Layla Thuluth are bundled under OFL with notices. Noto Sans is an explicit Latin fallback; Arabic styles never silently select an unrelated font.

Layla Diwani 2.0 supports unvocalized PNG/outlined SVG typography only. Its original fsType=2 and missing GPOS are retained and enforced. See FONT_LICENSES.md for the pinned mirror, copyright and exact restrictions. Amiri, Aref Ruqaa and Reem Kufi remain future candidates, not implemented alternatives.

Layla Thuluth 2.0 is an unreleased addition with fsType=8, permitting embedded-font PDF as well as PNG and outlined SVG. Combining marks are refused because GPOS is absent. It shares the existing Layla license and provenance notices.
