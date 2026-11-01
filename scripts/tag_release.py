#!/usr/bin/env python3
"""Synchronized release tagger for the 12-module NumKit ecosystem.

Usage:
    python scripts/tag_release.py v1.0.0 [--push] [--dry-run]

Verifies that `numkit/bundle` and all 12 submodules under `modules/*` have
clean working trees, creates annotated tag `vX.Y.Z` across every submodule
and the bundle repository, and optionally pushes the tag to `origin`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"

SUBMODULES = (
    "value",
    "sys",
    "ops",
    "numkit",
    "codegen",
    "signal",
    "wavelet",
    "stats",
    "control",
    "audio",
    "comm",
    "image",
)

SEMVER_RE = re.compile(r"^v\d+\.\d+\.\d+$")


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Create synchronized release tags across all NumKit modules.")
    ap.add_argument("tag", help="Release tag in vMAJOR.MINOR.PATCH format (e.g. v1.0.0)")
    ap.add_argument("--push", action="store_true", help="Push the created tags to origin")
    ap.add_argument("--dry-run", action="store_true", help="Validate repositories without creating/pushing tags")
    args = ap.parse_args()

    tag = args.tag.strip()
    if not SEMVER_RE.match(tag):
        print(f"error: tag '{tag}' must match vMAJOR.MINOR.PATCH (e.g. v1.0.0)", file=sys.stderr)
        return 1

    repos: list[tuple[str, Path]] = [(f"modules/{m}", MODULES / m) for m in SUBMODULES]
    repos.append(("bundle", ROOT))

    # 1. Verify all repositories exist and have clean working trees
    for label, path in repos:
        if not path.exists():
            print(f"error: repository missing: {label} ({path})", file=sys.stderr)
            return 1
        st = run_git(path, "status", "--porcelain")
        if st.returncode != 0:
            print(f"error: git status failed in {label}:\n{st.stderr}", file=sys.stderr)
            return 1
        if st.stdout.strip():
            print(f"error: working tree is not clean in {label}:\n{st.stdout}", file=sys.stderr)
            return 1

    print(f"All {len(repos)} repositories are clean.")
    if args.dry_run:
        print(f"[dry-run] Would tag {len(repos)} repositories with '{tag}'"
              + (" and push to origin." if args.push else "."))
        return 0

    # 2. Create annotated tags
    msg = f"NumKit {tag}"
    for label, path in repos:
        res = run_git(path, "tag", "-a", tag, "-m", msg)
        if res.returncode != 0:
            print(f"error: failed to tag {label} with {tag}:\n{res.stderr}", file=sys.stderr)
            return 1
        print(f"  tagged {label:<18} -> {tag}")

    # 3. Push tags if requested
    if args.push:
        for label, path in repos:
            res = run_git(path, "push", "origin", tag)
            if res.returncode != 0:
                print(f"error: failed to push tag {tag} in {label}:\n{res.stderr}", file=sys.stderr)
                return 1
            print(f"  pushed {label:<18} -> origin/{tag}")

    print(f"\nRelease tag {tag} complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
