# Plan for v0.1.0-rc.3

RC2 adds limited Diwani typography at the owner’s request. RC3 should prioritize correctness, installation and feedback before expanding style coverage further. This plan is ordered by priority; it is not a promise that all twenty traditions will be implemented next.

| Priority | Work | Acceptance evidence |
|---|---|---|
| P0 | PDF-001: investigate glyph-to-Unicode mappings, reading order and smaller ActualText spans | Correct logical Arabic extraction for the declared supported reader/version matrix; tests for plain Arabic, diacritics, lam-alif, punctuation and mixed Latin/numbers; matching visual and embedded-font checks |
| P0 | Define PDF search, selection and copy/paste support | Manually test at least Chrome PDF viewer and a desktop reader, plus automated Poppler/pypdf extraction; record exact versions and unsupported behavior; never reverse source strings to hide extraction defects |
| P1 | Improve Diwani workflow limits | Vet a font/revision with suitable embedding flags and mark positioning before enabling PDF or harakat; never rename another script as Diwani |
| P1 | Review the manual Square Kufic grid study | Validate the actual letterforms and source mapping with the user; design a packed composition with a documented reading path before considering automatic text support; see [workflow and follow-up plan](square-kufic.md) |
| P1 | Incorporate RC2 user feedback | Reproduce reported spelling, clipping, layout, sizing and installation defects; add regression cases for material bugs |
| P1 | Verify skill installation and agent execution | Install from the tagged GitHub source with current Skills CLI; invoke an actual rendering workflow in Codex, Claude Code and Cursor where available; record supported/untested hosts |
| P1 | Expand runtime coverage | CI on Python 3.11–3.13 where dependencies support it, clean wheel/source installation, explicit native dependency diagnostics |
| P1 | Complete repository administration | Apply and verify main protection with quality/security checks, no force push/deletion, solo-maintainer PR policy, security settings and manual stable-release approval |
| P2 | Strengthen visual/layout review | Check long subtitles/names, dense harakat, Nastaliq collisions and different aspect ratios; record qualified review separately from software checks |
| P2 | Improve historical references | Replace provisional notes with school-specific scholarship; no numerical proportions without evidence |

## RC3 exit criteria

- Required automated tests and dependency audit pass on the exact tagged commit.
- PDF-001 is fixed for a documented reader matrix, or remains prominently experimental with a precise evidence-backed limitation. A stable release still requires the PDF correctness gate to pass.
- RC2 feedback has a disposition: fixed, reproduced with a planned fix, or explicitly unsupported.
- Source, wheel, examples, accuracy report and SHA-256 checksums correspond to the same commit.
- Release notes distinguish implemented typography, reference-only traditions, technical validation and expert authenticity review.
- Repository owner explicitly approves RC3 publication; RC2 authorization does not authorize future releases.

## Deferred beyond RC3

Aref Ruqaa integration, automatic Square Kufic text composition (the manual study exporter is a development preview), additional traditions and independent calligraphy certification remain separate projects. They must not distract from text correctness and installation reliability.
