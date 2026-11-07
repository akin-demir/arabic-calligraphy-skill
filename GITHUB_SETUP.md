# GitHub setup and main protection

Checked on 2026-11-07: the repository is private, RC4 is the current authorized candidate, and `main`
is **not protected**. The rulesets API returned HTTP 403 with:

> Upgrade to GitHub Pro or make this repository public to enable this feature.

The connected GitHub app has no administration write tools, and the local `gh`
credential is invalid. Neither committing workflow files nor this policy applies
branch protection. No protection or visibility change is claimed.

## Apply the prepared policy

The owner previously authorized public visibility. An administrator must either
make the repository public in [General settings](https://github.com/akin-demir/arabic-calligraphy-skill/settings)
or enable a GitHub plan that supports private repository protection.

With an authenticated administrator `gh` session and a supported repository plan:

```bash
gh api --method PUT repos/akin-demir/arabic-calligraphy-skill/branches/main/protection --input docs/main-protection.json
gh api repos/akin-demir/arabic-calligraphy-skill/branches/main/protection
```

The [prepared JSON](docs/main-protection.json) requires pull requests, current
`quality` and `security` checks, resolved conversations and admin enforcement;
it prevents force pushes and deletion. Zero additional approving reviews allows
a solo owner to merge their own PR after checks. Existing merge history is kept.
Inspect any existing policy before replacing it.

The same settings can be entered at [branch settings](https://github.com/akin-demir/arabic-calligraphy-skill/settings/branches).
To ensure only the owner can merge, also verify that other collaborators and apps
do not retain write/admin access. Requiring PRs alone does not restrict merging
to a named user; personal repositories do not support the organization-only push
restriction list. Do not claim owner-only merging until access is verified.

## Current workflow

Main is the trunk. Short-lived feature PRs run quality/security checks before
merging. The release candidate is built from its exact main commit with checksummed source, wheel,
skill ZIP, gallery and evidence. Historical release assets remain unchanged.
Future release publication still requires explicit owner authorization.

Completed branches are removed only after their work is merged or explicitly
superseded. The Thuluth trial is closed after negative visual feedback; dependency updates
are consolidated into RC4. Closed branch heads and reasons are recorded in
[the RC4 dispositions](docs/rc4-pr-resolutions.json). Cleanup preserves any branch
that moved or gained an open PR. The older Diwani README proposal was superseded
by the merged Square Kufic hero.
