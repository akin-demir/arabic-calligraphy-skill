# Release policy

The owner authorized the first private experimental release candidate, v0.1.0-rc.1, in this session. RC1 may be tried with PDF-001 explicitly documented. This authorization does not approve a stable release, another candidate, a repository visibility change or marketing publication.

## Experimental RC1

`release-plan.json` records the one-off scope. `verify_accuracy.py --candidate` requires all tests, font checks and exact semantic source mappings to pass, with the PDF extraction limitation explicitly accepted for RC1. Its report keeps `release_ready: false` while reporting candidate readiness separately. The normal `--release` stable gate remains strict and still fails on incorrect PDF extraction.

The RC1 workflow runs only on main when its release configuration is merged, builds and audits the exact commit, bundles checksummed source/wheel/examples/evidence, and publishes one private GitHub prerelease. It has read-only build permissions and grants contents write only to the publication job. It does not create a stable release, change visibility, overwrite an existing tag/release, or publish to PyPI. Subsequent candidates require new explicit owner approval and a reviewed change.

## Trunk-based development

Main is the trunk. Merge short-lived PRs after quality and security pass; retain the actual initial history with a merge commit. Tag release candidates from main. No develop or long-lived release branch is required. Repository-level protections must be applied and verified separately; workflow files do not establish those controls.

## Stable release gate

Before v0.1.0 stable: fix critical PDF extraction for documented target readers; run lint, all tests, gallery and `python scripts/verify_accuracy.py --release`; pass the dependency audit; verify installation, artifact/source identity, protections and release approval controls; and obtain explicit owner publication approval. Any authenticity claim additionally requires independent human review evidence. Never overwrite historical tags or releases.

See [RC1 notes](docs/releases/v0.1.0-rc.1.md), [RC2 plan](docs/next-candidate.md), [accuracy](ACCURACY.md) and [repository settings](GITHUB_SETUP.md).
