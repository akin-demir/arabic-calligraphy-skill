# Actual GitHub setup

Repository: akin-demir/arabic-calligraphy-skill. Inspected through the connected GitHub app on 2026-11-07. It is private; default branch is main. Visibility has not been changed. No release or marketing post has been published.

Applied and verified through the connector: initial README bootstrap on main, development branch, incremental implementation commits. The GitHub API transfer creates different remote commit IDs from the local Git commits; both histories reflect actual completed milestones. It is not a Git push preserving local object IDs. See ENGINEERING_REPORT.md for the remote history and PR.

Repository metadata/security/administration writes are not exposed by the connected app tools, and the shell GitHub credential is invalid. Description/topics, branch protection, required checks, security feature toggles, release reviewers and tag rules have NOT been applied or verified. Committing configuration files does not apply them. No credentials are included in source.

Prepared automation: `python scripts/configure_github.py --offline-plan` prints the intended settings without access. With a separately configured, authorized administrative gh login, run the script without flags to inspect/dry-run; `--apply` applies metadata/topics and a new main protection only when absence was established. Existing protection is preserved for manual review. The script never changes visibility or deletes branches/resources.

Proposed main policy: PRs required, zero additional approvals for solo maintenance, quality/security required checks, strict updates, admin enforcement, no force push or deletion. Protected branches for private repositories depend on GitHub plan. Preserve merge commits; disable squash of this initial history. Add Dependabot alerts, secret scanning/private reporting and code scanning where your plan supports them. Give Actions read-only default permissions. Enable immutable releases and tag rules where available after a maintainer reviews them.

Manual release environment: create production-release and configure required reviewers if available. Until confirmed, manual artifact review and explicit maintainer publication remain mandatory. Current workflow generates candidates only.

Draft PR #1 is open: https://github.com/akin-demir/arabic-calligraphy-skill/pull/1. Patched run 42353989686 passed quality and security; the earlier failed audit was resolved by requiring pypdf 6.21.4. This workflow result does not establish repository-level security toggles or protections.

## RC1 configuration and remaining administration

The owner authorized a first private testing candidate. The RC1 workflow builds/tests/audits before publishing one prerelease from main, with write permission scoped to the publication job. The stable gate remains strict. Main is the trunk; short PRs and versioned tags are the development/release policy. Dependabot configuration and minimal workflow permissions are committed.

Still requiring GitHub administrator access (not exposed by this connector; local gh authentication is invalid): repository description/topics, disabling squash for the initial history, main protection requiring PRs and quality/security, no force push/deletion, security feature toggles and stable-release environment reviewers. Repository visibility remains private. These settings are not claimed as applied. Run the existing inspect/apply script from an authenticated admin workstation, or use Settings → Branches/Rulesets and Security. Private branch protection can require a paid GitHub plan.
