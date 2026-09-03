#!/usr/bin/env python3
"""Release channel routing - read the project manifests and produce candidate channels.

    python scripts/route_release.py [--root .]

**This script only produces candidates; it makes no ruling.** On a shape conflict it reports
the conflict and leaves the decision to the user; where the shape is unknown it says so and
does not guess. The reasoning and the trade-offs are supplied by the agent, which needs
project context the script does not have.

Why it exists: the frozen template's stage 11 opens by stating that containers MUST NOT be
forced on mobile, desktop, SDK, library, plugin or embedded projects - and then spends the
rest of the section on Docker. Turning that warning into a routing step you cannot skip is
the only way the inertia gets blocked.

Standard library only; runs on both Windows and POSIX.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


class Channel:
    """The seven release channels. The first six come from the frozen template; the last
    covers the internal-network case."""

    CONTAINER = "container"
    PACKAGE_REGISTRY = "package-registry"
    APP_STORE = "app-store"
    INSTALLER = "installer"
    FIRMWARE = "firmware"
    HOSTING = "hosting-platform"
    PRIVATE_REGISTRY = "private-registry"


# Mutually exclusive groups: a project hitting two of these almost certainly has an
# under-specified shape rather than a genuine need to publish to both.
EXCLUSIVE = [
    {Channel.CONTAINER, Channel.APP_STORE},
    {Channel.CONTAINER, Channel.FIRMWARE},
    {Channel.APP_STORE, Channel.FIRMWARE},
]

MANIFESTS = ("package.json", "pyproject.toml", "Cargo.toml", "go.mod",
             "pom.xml", "build.gradle", "build.gradle.kts")


@dataclass
class Routing:
    channels: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    unknown: bool = False
    signals: list[str] = field(default_factory=list)


def _has(root: Path, *names: str) -> bool:
    return any((root / n).is_file() for n in names)


def _glob(root: Path, pattern: str) -> bool:
    return any(root.glob(pattern))


def _package_json_shape(root: Path) -> tuple[set[str], list[str]]:
    """An npm project: main or exports means a library, bin means a CLI; both go to a registry."""
    chans, sig = set(), []
    p = root / "package.json"
    if not p.is_file():
        return chans, sig
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return chans, ["package.json failed to parse; shape not judged"]
    for key in ("main", "exports", "bin"):
        if key in data:
            chans.add(Channel.PACKAGE_REGISTRY)
            sig.append(f"package.json has {key}")
    return chans, sig


def _pyproject_shape(root: Path) -> tuple[set[str], list[str]]:
    chans, sig = set(), []
    p = root / "pyproject.toml"
    if not p.is_file():
        return chans, sig
    text = p.read_text(encoding="utf-8")
    if re.search(r"^\s*\[project\.scripts\]", text, re.M):
        chans.add(Channel.PACKAGE_REGISTRY)
        sig.append("pyproject.toml has [project.scripts]")
    elif re.search(r"^\s*\[project\]", text, re.M):
        chans.add(Channel.PACKAGE_REGISTRY)
        sig.append("pyproject.toml has [project]")
    return chans, sig


def route(root: Path) -> Routing:
    """Detect the artifact shape and return candidate channels. **No rulings, no guesses.**"""
    out = Routing()
    chans: set[str] = set()

    if _has(root, "Dockerfile", "docker-compose.yml", "compose.yaml"):
        chans.add(Channel.CONTAINER)
        out.signals.append("a Dockerfile or compose file is present")

    if _glob(root, "*.podspec") or _glob(root, "*.xcodeproj") or _has(root, "AndroidManifest.xml"):
        chans.add(Channel.APP_STORE)
        out.signals.append("a mobile project or podspec is present")

    for probe in (_package_json_shape, _pyproject_shape):
        c, s = probe(root)
        chans |= c
        out.signals += s

    if _has(root, "Cargo.toml"):
        chans.add(Channel.PACKAGE_REGISTRY)
        out.signals.append("Cargo.toml is present")

    if _glob(root, "*.ino") or _has(root, "platformio.ini"):
        chans.add(Channel.FIRMWARE)
        out.signals.append("an embedded project file is present")

    if _has(root, "vercel.json", "netlify.toml", "fly.toml", "Procfile"):
        chans.add(Channel.HOSTING)
        out.signals.append("a hosting platform configuration is present")

    # Conflicts: report only, never choose.
    for group in EXCLUSIVE:
        hit = group & chans
        if len(hit) > 1:
            out.conflicts.append(
                "shape conflict: hits both " + " and ".join(sorted(hit))
                + " - say what this project actually produces; this script will not choose for you")

    out.channels = sorted(chans)
    # No manifest, or a manifest with no readable shape signal - both count as unknown, and
    # unknown is never guessed at.
    out.unknown = not chans
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Release channel routing (candidates only, no rulings)")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    r = route(Path(args.root))

    print("# Release channel routing - candidates")
    print()
    if r.unknown:
        print("**Shape unknown** - no determinable artifact shape was read from the manifests.")
        print()
        print("Say what this project actually produces (service / library / CLI / mobile app /")
        print("firmware and so on). **This script does not guess.**")
    else:
        print("| Candidate channel |")
        print("|---|")
        for c in r.channels:
            print(f"| {c} |")
    if r.signals:
        print()
        print("## Signals it rested on")
        for s in r.signals:
            print(f"- {s}")
    if r.conflicts:
        print()
        print("## Conflicts (for you to rule on)")
        for c in r.conflicts:
            print(f"- {c}")
    print()
    print("> Candidates are not a conclusion. The reasons for the choice, and for the")
    print("> rejections, are supplied by the agent and confirmed by you.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
