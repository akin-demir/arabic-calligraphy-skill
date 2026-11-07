# Font assets

Runtime assets live in `src/arabic_calligraphy/data/fonts/` so wheels work offline. The source/version/hash manifest is `src/arabic_calligraphy/data/fonts.json`. All bundled files are unmodified Debian Noto fonts, with OFL notices alongside them. Noto Sans is an explicit Latin fallback; other fonts are not silently selected.

Amiri (https://github.com/aliftype/amiri), Aref Ruqaa (https://github.com/aliftype/aref-ruqaa), and Reem Kufi (https://github.com/aliftype/reem-kufi) are reputable candidates. None is bundled or technically verified in this release. Aref Ruqaa must be added and tested before enabling Ruqah. An unrelated Naskh font is not a substitute.
