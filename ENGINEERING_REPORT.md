# Engineering handoff — 2026-11-07

## Implementation

Local repository: /workspace/arabic-calligraphy-skill. GitHub: https://github.com/akin-demir/arabic-calligraphy-skill. Development branch: feat/initial-arabic-calligraphy-skill. Draft PR: https://github.com/akin-demir/arabic-calligraphy-skill/pull/1. No merge, public release, tag, PyPI publication, skills.sh listing or marketing posting has been performed.

A working Python CLI/API and portable Agent Skill use Pango/HarfBuzz and Cairo for offline rendering. PNG, outlined SVG, embedded-font PDF, posters, wordmarks, certificates and paginated new documents are implemented. All 20 requested traditions have separate introductory references and machine-readable capability entries. Naskh, modern Kufic and Nastaliq Urdu are implemented as Approximate typography; the other 17 are Reference Only. Three workflows passed technical checks within their recorded scope; none has expert authenticity approval. Some history entries are provisional and school-specific numerical proportions remain unresearched.

Font integrity, glyph coverage, warnings for explicit Latin fallback, overflow errors and atomic output writes are implemented. SVG retains exact input in descriptive metadata; PDF includes semantic ActualText mappings, but raw reader extraction remains a known limitation. The API is not thread-safe for concurrent use in one process because font configuration is process-global. Linux is the tested platform. See ACCURACY.md and docs/architecture.md for boundaries.

## Validation

374 local tests passed with zero failures, errors or skips. 113 Unicode inputs are checked in all three implemented fonts. Other tests cover fonts, capabilities, input bounds, exports, alpha, clipping bounds, overflow, atomic writes, CLI behavior, page counts and raster fixtures. Tests exercise marks, hamzas, lam-alif, joining combinations, controls, numbers, mixed scripts, multiline and wrapped text. Automated tests do not establish artistic authenticity or perfect mark placement in every possible string.

Python syntax/whitespace checks, metadata/registry lint and JSON/YAML/TOML parsing pass. The original local test runtime was Python 3.12.14, pypdf 6.10.0, Pango 1.56.3 and Cairo 1.18.4. That pypdf version was later rejected by the remote security audit; the package now requires at least 6.21.4 and the development toolchain pins 6.21.4. The original snapshot in docs/validation is clearly labeled; it is not evidence of testing the patched dependency locally.

The wheel built and an installed-wheel CLI SVG render passed in a separate venv sharing the host dependencies. A clean dependency installation is exercised by GitHub Actions, rather than claimed from that shared-dependency venv. Native raster references are versioned; gallery PNG/SVG/PDF outputs are actual engine files. Human software visual review covered Naskh, Nastaliq and the poster. No calligrapher review has been obtained.

Initial GitHub run https://github.com/akin-demir/arabic-calligraphy-skill/actions/runs/42353742850: quality passed (installation, tests, gallery, build and artifact upload); security failed with 49 pypdf advisories. Dependency minimum/pin was raised in remote commit 4c2c1e5 to the latest required fix version reported by the audit, 6.21.4. Patched run https://github.com/akin-demir/arabic-calligraphy-skill/actions/runs/42353989686 passed both quality and security. It ran the then-current 365 tests with pypdf 6.21.4, Python 3.12.16, Pango 1.52.1 and Cairo 1.18.0; the audit reported no known vulnerabilities. Nine additional carriage-return/layout checks were added afterward, bringing the local suite to 374. No audit is suppressed and the security gate remains required by the proposed policy.

Exact raw pypdf Arabic extraction fails on the original three PDF samples even though source mappings and font embedding pass. `verify_accuracy.py --release` exits 1. This failure is deliberate evidence, not a successful release check.

## Actual development history through the final layout fix

These are real milestone commits, created incrementally as work was completed. The network sandbox prevented Git transport; the connected API transferred each milestone onto a bootstrapped remote branch. Remote commit hashes differ from local object IDs. No timestamps were backdated and the implementation was not squashed into a single commit.

| Local commit | Remote commit | Milestone |
|---|---|---|
| — | 0ca48aba | Bootstrap empty repository with README |
| 359c24e | 12a2cbca | Initialize packaging and portable skill |
| d4c46ca | 12c3afa7 | Catalog traditions and licensed fonts |
| c77c4eb | 022f1650 | Native Arabic rendering exports |
| 5c6587a | ea5ce019 | CLI, layouts, PDF semantic mappings |
| a7774c2 | c37de1f8 | Unicode/export/visual tests and gallery |
| 6fa28c4 | 833d0f9a | CI, evidence reports and configuration plan |
| 0463d17 | 4c2c1e5f | Require security-patched pypdf |
| 443c7df | 1a573504 | Preserve carriage returns and scaled layout bounds |

This table is a snapshot before the documentation/report commit containing this file. Use `git log --oneline --reverse` or the PR Commits tab for the complete final history, including subsequent documentation and CI corrections. The local branch remains separate from the API-created remote history; do not force-push it over the remote. A future checkout should clone the remote feature branch.

## GitHub, distribution and launch

The repository remains private with main as default. Implementation is on the feature branch, and PR #1 is a draft. Administration tools for metadata writes, protection, security toggles, release environments and tag policies are unavailable through this connection; shell gh authentication is invalid. Those settings are NOT claimed as applied. GITHUB_SETUP.md records the proposed settings, limits and reproducible inspection/apply script. No visibility change or protection bypass occurred.

Agent Skills frontmatter and reference structure are checked locally. Codex/Claude Code/Cursor methods were researched from official sources and documented, but host execution was not tested. The intended Skills CLI GitHub command applies after merge and requires authentication while private. No remote Skills CLI installation or skills.sh discovery claim is made. Marketing announcements, human-authored Reddit notes and a real-output storyboard are drafts only.

## Release decision

**NOT READY — BLOCKERS REMAIN.** Resolve exact PDF extraction for the documented target readers, pass patched-dependency remote quality/security checks, verify required GitHub settings and Skills CLI/host installation, and obtain explicit maintainer approval before publication. The manual candidate workflow reruns a strict release gate and produces artifacts only; it never publishes automatically. Do not promote reference-only traditions or claim classical authenticity to make a release matrix look complete.

## Subsequent owner-authorized RC1 decision

The owner requested a first private release candidate for testing before continuing. Experimental RC1 publication is now authorized with PDF-001 disclosed; this supersedes the earlier prohibition on any candidate publication, while leaving the stable PDF gate and future-release approval intact. RC1 assets are built from the exact main commit by GitHub Actions. See release-plan.json, RC1 notes and the RC2 plan. Repository administration controls remain unapplied where the connection lacks capability.

## RC2 Diwani increment

The owner requested Diwani implementation and a new release candidate. RC2 adds unmodified OFL LaylaDiwani Regular 2.0, with a pinned mirror, author/license notices and exact hash. Its original fsType=2 and absent GPOS are preserved: only unvocalized PNG and outlined SVG are enabled; PDF/harakat are explicitly refused. No Jali or custom logo composition is claimed. All 470 local tests pass, including 89 Diwani corpus inputs, export-policy checks and a raster fixture. The local host still has old pypdf; the exact tagged candidate is rebuilt and audited with the patched dependency in GitHub Actions. RC1 and its release history remain immutable. The remaining plan is now RC3 in docs/next-candidate.md.
