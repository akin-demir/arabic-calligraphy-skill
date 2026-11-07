# Release procedure

Current decision: NOT READY — PDF extraction and external verification blockers remain. The package version is a candidate, not a published release.

1. Fix all critical text integrity/extraction defects. Run repository lint, all tests, gallery generation and `python scripts/verify_accuracy.py --release`. The strict gate currently fails honestly on extraction.
2. Update CHANGELOG, version, capabilities, font manifest and accuracy evidence together. Any claimed authentic style needs independent human review evidence.
3. Build from a clean checkout with `python -m build`; inspect wheel/sdist contents and install the wheel into a fresh environment. Run actual CLI rendering there. Record dependency versions and artifact hashes.
4. Ensure remote quality/security checks pass for the exact commit. Verify settings in GITHUB_SETUP.md, including required checks, release environment reviewers and tag protection. Do not bypass restrictions unsupported by a private repository plan; document a maintainer-controlled manual process instead.
5. Obtain explicit maintainer approval for a versioned tag and release. A maintainer may then create and push an immutable version tag. Never overwrite an existing tag/release.
6. Run the manual candidate workflow for that existing tag. It checks out the tag, reruns gates and builds an artifact; it never publishes automatically.
7. A maintainer reviews the downloaded artifact and creates a draft GitHub Release with changelog, date, supported matrix, accuracy JSON, font/dependency info, installation instructions, examples and known limitations. Obtain explicit approval before making that draft public. Verify artifacts correspond to the tagged source. Do not publish to PyPI as an incidental step.
8. Test `npx skills add akin-demir/arabic-calligraphy-skill` against the merged authorized repository and target hosts. Verify any skills.sh listing before announcing it. Publish marketing only with separate authorization.

Use the `production-release` GitHub environment with required reviewers where the plan permits. The workflow does not rely on environment creation to establish approval: it creates no public release even if the environment has no reviewer rule. See .github/RELEASE_TEMPLATE.md for content. Preserve meaningful development history in a non-squash merge.
