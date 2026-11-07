"""Owner-authorized RC3 cleanup. Delete only named, merged, inactive branches.

Run after RC3 publication. Dry-run unless --apply is supplied. Never delete work
with an open PR, an unexpected head, or commits absent from the released source.
"""

import argparse
import json
import os
import re
import subprocess

REPO = "akin-demir/arabic-calligraphy-skill"
BRANCHES = {
    "feat/initial-arabic-calligraphy-skill": "24ac0b3d5d0915102411680b690ca863d5959253",
    "feat/diwani-rc2": "c03df6262517607dfa0705df94323775a5bc21d2",
    "feat/square-kufic": "4dfa9d42366d890e5a69ea2b0b783e8bcf59c280",
    "feat/rc3-release": None,
}


def api(path, method="GET"):
    result = subprocess.check_output(["gh", "api", "--method", method, f"repos/{REPO}/{path}"], text=True)
    return json.loads(result) if result.strip() else None


def cleanup(source, apply=False):
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        raise ValueError("Expected exact released source SHA")
    release = api("releases/tags/v0.1.0-rc.3")
    if release.get("draft") or not release.get("prerelease"):
        raise ValueError("Published RC3 prerelease is required before cleanup")
    tag = api("git/ref/tags/v0.1.0-rc.3")
    if tag["object"]["type"] != "commit" or tag["object"]["sha"] != source:
        raise ValueError("RC3 tag must identify the checked source commit")
    report = []
    for branch, expected in BRANCHES.items():
        # Listing refs makes already-deleted branches harmless on a repeated run.
        refs = api(f"git/matching-refs/heads/{branch}")
        matches = [r for r in refs if r["ref"] == f"refs/heads/{branch}"]
        if not matches:
            report.append(dict(branch=branch, result="already absent"))
            continue
        sha = matches[0]["object"]["sha"]
        if expected and sha != expected:
            report.append(dict(branch=branch, result="kept: head changed"))
            continue
        prs = api(f"pulls?state=open&head=akin-demir:{branch}&per_page=1")
        comparison = api(f"compare/{sha}...{source}")
        if prs or comparison.get("status") not in ("ahead", "identical"):
            report.append(dict(branch=branch, result="kept: active or unmerged"))
            continue
        current = api(f"git/ref/heads/{branch}")["object"]["sha"]
        if current != sha:
            report.append(dict(branch=branch, result="kept: changed during inspection"))
            continue
        if apply:
            api(f"git/refs/heads/{branch}", "DELETE")
        report.append(dict(branch=branch, sha=sha, result="deleted" if apply else "would delete"))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(cleanup(os.environ["SOURCE_COMMIT"], args.apply), indent=2))
