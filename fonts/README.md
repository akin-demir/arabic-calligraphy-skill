# Bundled fonts

Runtime assets live in src/arabic_calligraphy/data/fonts/ so wheels work offline. The source/version/hash manifest is src/arabic_calligraphy/data/fonts.json. Four unmodified Noto families and Layla Diwani are bundled under OFL with notices. Noto Sans is an explicit Latin fallback; Arabic styles never silently select an unrelated font.

Layla Diwani 2.0 supports unvocalized PNG/outlined SVG typography only. Its original fsType=2 and missing GPOS are retained and enforced. See FONT_LICENSES.md for the pinned mirror, copyright and exact restrictions. Amiri, Aref Ruqaa and Reem Kufi remain future candidates, not implemented alternatives.
