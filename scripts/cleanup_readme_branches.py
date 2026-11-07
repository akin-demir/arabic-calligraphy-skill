"""One-off owner-authorized cleanup while preparing the Square Kufic README.

Preserve active/moved branches. The old Diwani proposal is explicitly superseded;
all other cleanup targets must be merged into the inspected main source commit.
"""

import argparse
import json
import os
import re
import subprocess

REPO = "akin-demir/arabic-calligraphy-skill"
OLD = "659676bbf67909f4d239382b20660505aa22fb4b"


def api(path, method="GET"):
    result = subprocess.check_output(["gh", "api", "--method", method, f"repos/{REPO}/{path}"], text=True)
    return json.loads(result) if result.strip() else None


def cleanup(source, apply=False):
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        raise ValueError("An exact inspected source SHA is required")
    report = []
    for branch in ("feat/readme-diwani", "feat/readme-square-kufic"):
        matches = [r for r in api(f"git/matching-refs/heads/{branch}")
                   if r["ref"] == f"refs/heads/{branch}"]
        if not matches:
            report.append(dict(branch=branch, result="already absent"))
            continue
        sha = matches[0]["object"]["sha"]
        if api(f"pulls?state=open&head=akin-demir:{branch}&per_page=1"):
            report.append(dict(branch=branch, result="kept: open PR"))
            continue
        if branch == "feat/readme-diwani":
            pr = api("pulls/10")
            safe = sha == OLD and pr["state"] == "closed" and pr["head"]["sha"] == OLD
        else:
            prs = api(f"pulls?state=closed&head=akin-demir:{branch}&per_page=100")
            safe = (any(p.get("merged_at") and p["head"]["sha"] == sha for p in prs)
                    and api(f"compare/{sha}...{source}").get("status") in ("ahead", "identical"))
        if not safe or api(f"git/ref/heads/{branch}")["object"]["sha"] != sha:
            report.append(dict(branch=branch, result="kept: moved or unmerged"))
            continue
        if apply:
            api(f"git/refs/heads/{branch}", "DELETE")
        report.append(dict(branch=branch, result="deleted" if apply else "would delete", sha=sha))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(cleanup(os.environ["SOURCE_COMMIT"], args.apply), indent=2))
