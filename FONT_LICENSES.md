# Font licenses

Original code is MIT; font binaries retain SIL Open Font License 1.1. Fonts are unmodified. Redistribution requires keeping the accompanying license, attribution and reserved font names. Font designs remain their authors' property.

## Four Noto fonts

Noto Naskh Arabic, Noto Kufi Arabic, Noto Nastaliq Urdu and Noto Sans are unmodified Debian fonts-noto-core 20201225-2 binaries. Their fsType is 0; embedding is enabled for their PDF workflows. Full Debian copyright and OFL notices remain in OFL-and-notices.txt. Source: https://github.com/notofonts/noto-fonts .

## Layla Diwani — new in RC2

LaylaDiwani Regular 2.0 is by Mohammed Isam, copyright 2014–2017. Its internal notice credits Latin glyphs and numbers to Basharat Ali's Urdu Khush Khati 1.5, also under OFL. Full OFL, reserved names, author file, FONTLOG and mirror provenance are bundled as Layla-OFL.txt, Layla-Authors, Layla-FONTLOG.txt and Layla-SOURCE.md. Official project listing: https://fontlibrary.org/en/font/layla-diwani . Fedora's font audit independently lists the same OFL family: https://fedoraproject.org/wiki/I18N/Fonts/Audit .

Retrieval mirror: NazirNayal8/nazirnayal.github.io, pinned commit d00ad06f30de6557a61bfe1e9bcdd4873eb4f7c7, assets/fonts/layla/. SOURCE.md identifies ALT Linux fonts-ttf-layla 2.0-alt1_2. Runtime verifies the bundled font hash before registering it.

The original font's fsType=2 conflicts with general OFL embedding permission. We do not change its bytes or override that technical flag: Diwani PDF embedding/export is disabled. Only PNG and outlined SVG are supported. The manifest distinguishes license_embedding_permission from enabled embedding_permission. No GPOS is present, so combining marks are explicitly refused. This is an implementation boundary, not an assertion that the OFL prohibits embedding.

## Exact font records

- **Noto Naskh Arabic Regular**: 2.004; ttfautohint (v1.8.3) -l 8 -r 50 -G 200 -x 14 -D arab -f none -a qsq -X ""; fsType 0; SHA-256 `8c67eaa2f0086872628fc3f7f760386f83c8be5c5e9a1ba3a38891237b2ac7cb`.
- **Noto Kufi Arabic Regular**: Version 2.102; ttfautohint (v1.8.3) -l 8 -r 50 -G 200 -x 14 -D arab -f none -a qsq -X ""; fsType 0; SHA-256 `befb9d07506942ba2a7e0e85c65a24a76792c937d812bc80f1095d0f660cf330`.
- **Noto Nastaliq Urdu Regular**: Version 2.000; ttfautohint (v1.8.3) -l 8 -r 50 -G 200 -x 14 -D arab -f none -a qsq -X ""; fsType 0; SHA-256 `fe24c4a05b19482beac11e4b90a0f6754214f1cb5e925cf9e86b48283ac37522`.
- **Noto Sans Regular**: Version 2.004; ttfautohint (v1.8.3) -l 8 -r 50 -G 200 -x 14 -D latn -f none -a qsq -X ""; fsType 0; SHA-256 `89c3c497f618fdaa0b2d1e98fef93582f28c71debd2c4a8cdf41f190ced2909d`.
- **LaylaDiwani Regular**: Version 2.0; fsType 2; SHA-256 `089116f093e8e79ffd76f53c89dee1b4040d15d5568e1ecbafc937f8acb9b27b`.
