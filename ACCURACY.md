# Accuracy and release evidence

Local candidate validation on 2026-11-07: **374 passed, 0 failures, 0 errors, 0 skipped**. The corpus contains 113 distinct Unicode scenarios, each rendered in all three implemented fonts. Run `PYTHONPATH=src python scripts/verify_accuracy.py` to reproduce JSON, JUnit totals, full test log, font checks and PDF extraction observations in reports/. Committed snapshots are in docs/validation/.

| Dimension | Evidence and scope | Result |
|---|---|---|
| Catalog | Unique entries with separate references | 20 documented; four introductory entries explicitly provisional |
| Implemented styles | Naskh, modern Kufic, Nastaliq Urdu typography | 3 |
| Technical verification | Local corpus, native glyph checks, bounds, export, fonts and raster fixtures | 3, limited to documented scope |
| Public classification | No independent artistic review | 3 Approximate; 17 Reference Only; 0 Verified |
| Expert authenticity | No consenting qualified reviewer evidence supplied | 0 |
| Source integrity | Exact SVG description against original codepoints, no normalization/reversal | 339 corpus/font checks pass |
| Coverage | fontTools cmap validation and Pango unknown-glyph check | Checked for every rendering |
| Exports | Actual PNG, paths in SVG, native PDF; poster/certificate/document samples | Pass locally |
| PDF embedding | FontFile2/FontFile3 streams in exported font descriptors | Pass |
| PDF logical mapping | ActualText associated with real drawn glyphs, UTF-16 source matches | Pass for sampled texts |
| Generic PDF extraction | pypdf 6.10.0 output compared with exact original | Fails exact Arabic order for three samples; release blocker |
| Visual fixtures | Three versioned PNG references; cropped ink image-difference comparison | Pass on local runtime |
| Font licensing | Four hashes, OFL notices, fsType 0 and GSUB/GPOS checks | Pass |

The 374 total combines corpus tests with registry, coverage, invalid configuration, export, atomic writes, CLI, layouts and regression checks. It does not count 374 expert artistic judgments. The test suite intentionally separates exact PDF semantic-source mapping from raw reader extraction; a green ordinary suite is not permission to release. `--release` adds the unresolved extraction gate and currently returns nonzero.

Tests show known inputs preserve source text and produce measurable artifacts, not that every Arabic string looks perfect. Mark collision detection and detailed calligraphic proportions require qualified visual review. Pango unknown-glyph checks detect missing glyphs, not incorrect artistic decisions. PNG has no searchable text; SVG text is descriptive metadata, not editable live lettering. Page-level PDF ActualText can have reader-dependent effects on selection granularity.

Native reference runtime: Python 3.12.14; Pango 1.56.3; Cairo 1.18.4; HarfBuzz 10.2.0. Font bytes and versions are pinned in the manifest. CI records output under its own OS library versions; the visual tolerance permits small antialiasing differences, not arbitrary redraws. No cross-platform determinism claim is made.

Human inspection in this session covered the actual Naskh sample, poster and Nastaliq sample. This is a general software visual check, not independent calligraphy expertise. Native shaping/ligatures/diacritics are exercised by the corpus, but no expert claims of universal mark positioning are made. Historical references are introductory; Sunbuli attribution and school-specific details remain under research.

Wheel build and a CLI render from an installed wheel passed in a separate venv using shared host dependencies. Clean dependency/package installation passed in GitHub Actions on Ubuntu with patched pypdf 6.21.4. End-to-end agent host execution and Skills CLI GitHub installation remain unverified. Remote CI and vulnerability audit results are tracked in ENGINEERING_REPORT.md; do not infer them from local tests.

**Release decision: NOT READY — BLOCKERS REMAIN.** Exact reader text extraction, remote quality/security validation, repository administration verification and explicit maintainer publication approval are outstanding. No public release, tag, PyPI package, skills.sh listing or marketing publication is claimed.
