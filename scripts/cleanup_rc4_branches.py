"""Owner-authorized RC4 cleanup. Delete only named, finalized, inactive branches.

Run after RC4 publication. Dry-run unless --apply is supplied. Never delete work
with an open PR or an unexpected head. Unmerged branches require an explicit
closed-PR disposition in the RC4 resolution record.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

REPO = "akin-demir/arabic-calligraphy-skill"
RESOLUTIONS = {item["branch"]: item for item in json.loads(
    (Path(__file__).resolve().parents[1] / "docs/rc4-pr-resolutions.json").read_text())}
BRANCHES = {
    "feat/readme-square-kufic": "76b92022f6eafc712f211181b8fa834059a1064d",
    "feat/rc4-release": None,
    **{branch: item["sha"] for branch, item in RESOLUTIONS.items()},
}


def api(path, method="GET"):
    result = subprocess.check_output(["gh", "api", "--method", method, f"repos/{REPO}/{path}"], text=True)
    return json.loads(result) if result.strip() else None


def cleanup(source, apply=False):
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        raise ValueError("Expected exact released source SHA")
    release = api("releases/tags/v0.1.0-rc.4")
    if release.get("draft") or not release.get("prerelease"):
        raise ValueError("Published RC4 prerelease is required before cleanup")
    tag = api("git/ref/tags/v0.1.0-rc.4")
    if tag["object"]["type"] != "commit" or tag["object"]["sha"] != source:
        raise ValueError("RC4 tag must identify the checked source commit")
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
        if branch in RESOLUTIONS:
            pr = api(f"pulls/{RESOLUTIONS[branch]['number']}")
            finalized = pr["state"] == "closed" and pr["head"]["sha"] == sha
        else:
            finalized = api(f"compare/{sha}...{source}").get("status") in ("ahead", "identical")
        if prs or not finalized:
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
