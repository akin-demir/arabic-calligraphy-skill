# RC2 accuracy and release evidence

**470 local tests pass, with no failures, errors or skipped tests.** The existing corpus has 113 scenarios rendered in Naskh, modern Kufi and Nastaliq. Diwani adds 89 unmarked inputs, PNG/SVG export checks, explicit refusal of missing coverage, combining marks and PDF, and a visual reference. There are twenty documented traditions: four approximate implemented font workflows, sixteen reference-only, zero expert-authenticity certifications.

## Diwani scope

LaylaDiwani Regular 2.0 is bundled unchanged under OFL with author notices, FONTLOG, exact hash and pinned provenance. It has GSUB but no GPOS and fsType=2. Technical validation is limited to unvocalized PNG/outlined SVG. The runtime refuses harakat and PDF instead of claiming unverified positioning or overriding the embedding flag. No Diwani Jali or custom emblem composition is implemented. General software visual inspection covered the actual Diwani sample and poster; no expert calligraphy review has occurred.

## Other workflows

The Noto workflows retain existing PNG/SVG/PDF functionality. Font coverage, unknown glyphs, source metadata, dimensions, alpha, atomic writes, embedding, pagination, CLI and visual regression checks pass locally. They do not prove that every possible Arabic composition is correct. PDF-001 remains: raw Arabic extraction can reorder text and marks even though logical ActualText mappings and embedded fonts are present. `--release` remains blocked. `--candidate` records the owner's RC2 testing approval separately and never sets stable readiness true.

## Reproduction and environment

Run `python scripts/check_project.py`, `PYTHONPATH=src python scripts/verify_accuracy.py --candidate`, and `PYTHONPATH=src python scripts/generate_gallery.py`. Reports are written to reports/. Local snapshots for RC2 are in docs/validation/rc2-*. The local host still has pypdf 6.10.0; the release dependency is pypdf 6.21.4 and the clean GitHub workflow verifies that patched runtime before publication. Do not treat the original host as the release runtime.

Fonts are hash-pinned. Native local versions are Pango 1.56.3 and Cairo 1.18.4; GitHub tests use its Ubuntu versions and versioned raster fixtures with a small antialiasing tolerance. The source/wheel/gallery/evidence/checksums and ready-to-upload skill ZIP are built for the exact tagged commit by the candidate workflow. Font licensing checks cover all five binaries, preserving the restricted Layla export policy.

## Release decision

RC2 is authorized for experimental testing with PDF-001 and DIWANI-001 disclosed. Stable release remains blocked on documented PDF correctness, target-reader/host verification and explicit stable publication approval. GitHub administrator settings and web-chat renderer execution remain unverified through this connection. No new artistic authenticity or skills.sh listing claim is made. RC1 assets are not rewritten.
