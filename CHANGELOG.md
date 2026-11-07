# Changelog

## Unreleased — 0.1.0rc3.dev0

- Add unchanged OFL LaylaThuluth 2.0, with shared notices and pinned hash/provenance.
- Implement unvocalized Thuluth PNG, outlined SVG and embedded-font PDF; preserve editable fsType=8 and refuse unsupported combining marks.
- Add actual Thuluth gallery samples, font-selection/embedding checks, visual fixture and 89 unmarked corpus inputs: 566 tests total.
- Require candidate authorization to match the implemented style list and installed version; stale RC2 approval cannot publish this feature.
- Historical/freeform composition and PDF-001 remain unresolved. No new release has been authorized or published.

## 0.1.0rc2 — Diwani experimental candidate

- Add unchanged OFL Layla Diwani 2.0 with full notices, hash and pinned provenance.
- Implement unvocalized Diwani PNG/outlined SVG lettering and posters; explicitly refuse PDF and combining marks.
- Expand to 470 tests and actual Diwani gallery/visual references.
- Add a ready-to-upload skill ZIP as a checksummed release asset.
- Clarify modern Kufi versus Square Kufic and prohibit renderer substitution by agents.
- Keep PDF-001 unresolved and stable publication gated; carry remaining work into the RC3 plan.

## 0.1.0rc1 — first experimental candidate

- Portable Agent Skill and 20 introductory tradition references.
- Bundled Noto Naskh, Kufi, Nastaliq Urdu and explicit Latin fallback font.
- Pango/Cairo PNG, outlined SVG and native PDF with embedded fonts and ActualText.
- CLI/API, posters, wordmarks, certificates and paginated plain-text documents.
- 365 local tests, real gallery and accuracy reports.
- Known blocker: exact Arabic text extraction is not consistent across PDF readers.

Pre-1.0 API changes may occur in minor releases; patch releases preserve documented behavior where feasible. The GitHub prerelease tag is v0.1.0-rc.1; stable release remains blocked. See the RC1 notes and RC2 plan.
