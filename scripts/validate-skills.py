#!/usr/bin/env python3
"""Validate the agent-engineering-skills repository.

Standard library only. No third-party dependencies.

Checks:
  1. Skill directories and SKILL.md files exist.
  2. YAML frontmatter present with name / description / version / license / metadata.
  3. `name` matches the directory name.
  4. Both skills share the same version (expected v2.2.0).
  5. All relative Markdown links inside skills/ resolve to existing files.
  6. No orphaned reference files (present but never referenced).
  7. Feature skill does not copy the full Base Protocol (duplication check).
  8. Basic Markdown structure is valid.

Exit code: 0 if no FAIL, 1 otherwise.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

EXPECTED_SKILLS = ["project-bootstrap-workflow", "feature-change-workflow"]
EXPECTED_VERSION = "2.2.0"

# Distinctive, long phrases that belong exclusively to the Base Protocol.
# They MUST NOT be redefined inside the feature skill files.
BASE_ONLY_SENTINELS = [
    "Backend 类型统一为三级",
    "Backend 初始化 MUST 遵循以下生命周期",
    "Code Graph 构建 MUST 按以下层级降级",
    "Agent MUST 使用三级定位协议",
    "Agent MUST 按以下顺序执行适用的验证",
]

results = []  # (level, message)


def report(level, message):
    results.append((level, message))


def ok(message):
    report("PASS", message)


def warn(message):
    report("WARNING", message)


def fail(message):
    report("FAIL", message)


def read_text(path):
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text):
    """Parse a minimal YAML frontmatter block into a dict of key -> raw value.

    Returns (dict, error). Does not use PyYAML; only needs top-level scalar keys.
    """
    lines = text.splitlines()
    if not lines:
        return None, "file is empty"
    if lines[0].strip() != "---":
        return None, "missing opening --- on first line"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "missing closing ---"
    keys = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    return keys, None


def clean_version(raw):
    return (raw or "").strip().strip('"').strip("'")


def headings(text):
    """Return a set of normalized ATX headings (#... ) from markdown text."""
    out = set()
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            out.add(re.sub(r"\s+", " ", m.group(2)).strip())
    return out


def extract_md_links(path):
    """Extract relative Markdown link targets (outside code fences)."""
    links = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"\]\(([^)\s]+)\)", line):
            links.append(m.group(1))
    return links


def main():
    print(f"Repo root: {REPO_ROOT}\n")

    # 1. Directory structure
    if not SKILLS_DIR.is_dir():
        fail(f"skills/ directory not found: {SKILLS_DIR}")
        finish()
        return
    ok("skills/ directory exists")

    skill_dirs = {}
    for name in EXPECTED_SKILLS:
        d = SKILLS_DIR / name
        skill_dirs[name] = d
        if d.is_dir():
            ok(f"skill directory exists: {name}")
        else:
            fail(f"skill directory missing: {name}")

    versions = {}

    # 2 & 3. SKILL.md + frontmatter + name match
    for name, d in skill_dirs.items():
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            fail(f"SKILL.md missing: {skill_md}")
            continue
        ok(f"SKILL.md exists: {name}")

        text = read_text(skill_md)
        fm, err = parse_frontmatter(text)
        if fm is None:
            fail(f"frontmatter invalid in {skill_md}: {err}")
        else:
            ok(f"frontmatter present: {name}")

        if fm is not None:
            for key in ("name", "description", "version", "license"):
                if key in fm and fm[key]:
                    ok(f"{name}: frontmatter has '{key}'")
                else:
                    fail(f"{name}: frontmatter missing '{key}'")
            # 'metadata' is a mapping key whose inline value may be empty;
            # only its presence is required.
            if "metadata" in fm:
                ok(f"{name}: frontmatter has 'metadata'")
            else:
                fail(f"{name}: frontmatter missing 'metadata'")

            if "name" in fm and fm["name"]:
                if fm["name"] == name:
                    ok(f"{name}: name matches directory")
                else:
                    fail(f"{name}: name '{fm['name']}' != directory '{name}'")

            if "version" in fm:
                versions[name] = clean_version(fm["version"])
                if versions[name] == EXPECTED_VERSION:
                    ok(f"{name}: version {EXPECTED_VERSION}")
                else:
                    fail(f"{name}: version '{fm['version']}' != {EXPECTED_VERSION}")

        # 8. Basic markdown structure
        if "\n# " in "\n" + text or text.lstrip().startswith("# "):
            ok(f"{name}: has top-level heading")
        else:
            fail(f"{name}: missing top-level (#) heading")

    # 4 & 9. Unified version
    if len(versions) == len(EXPECTED_SKILLS):
        if len(set(versions.values())) == 1 and versions.get(EXPECTED_SKILLS[0]) == EXPECTED_VERSION:
            ok(f"all skills share version {EXPECTED_VERSION}")
        else:
            fail(f"skills do not share a single version: {versions}")

    # 5 & 6. Reference links
    all_md_files = sorted(SKILLS_DIR.rglob("*.md"))
    referenced_targets = set()
    dead_links = []

    for md in all_md_files:
        for link in extract_md_links(md):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not link.endswith(".md"):
                continue
            # strip query/anchor if present
            link_path_part = link.split("#", 1)[0].split("?", 1)[0]
            target = (md.parent / link_path_part).resolve()
            if target.is_file():
                referenced_targets.add(target)
            else:
                dead_links.append(f"{md.relative_to(REPO_ROOT)} -> {link}")

    if dead_links:
        for item in dead_links:
            fail(f"dead link: {item}")
    else:
        ok("all relative markdown links resolve")

    # Orphaned reference files (present but never referenced)
    for name in EXPECTED_SKILLS:
        refs_dir = skill_dirs[name] / "references"
        if not refs_dir.is_dir():
            continue
        for ref_file in sorted(refs_dir.glob("*.md")):
            resolved = ref_file.resolve()
            if resolved not in referenced_targets:
                warn(f"reference file never referenced: {ref_file.relative_to(REPO_ROOT)}")

    # 7. Duplication check
    base_md = skill_dirs["project-bootstrap-workflow"] / "references" / "base-protocol.md"
    feature_files = [
        skill_dirs["feature-change-workflow"] / "SKILL.md",
        skill_dirs["feature-change-workflow"] / "references" / "feature-change.md",
    ]

    if base_md.is_file():
        # Section 1 (Role / 术语约束) is shared boilerplate present in both
        # source documents; it is not part of the Base Protocol's engineering
        # sections and must not trigger the duplication check.
        def is_section_one(h):
            return bool(re.match(r"^1(\.|\s)", h))

        base_headings = {h for h in headings(read_text(base_md)) if not is_section_one(h)}
        feature_headings = set()
        for f in feature_files:
            if f.is_file():
                feature_headings |= headings(read_text(f))

        overlap = base_headings & feature_headings
        if overlap:
            for h in sorted(overlap):
                fail(f"feature skill redefines Base Protocol heading: {h}")
        else:
            ok("no Base Protocol headings redefined in feature skill")

        feature_text = "\n".join(read_text(f) for f in feature_files if f.is_file())
        sentinel_hits = [s for s in BASE_ONLY_SENTINELS if s in feature_text]
        if sentinel_hits:
            for s in sentinel_hits:
                fail(f"feature skill appears to copy Base Protocol content: '{s}'")
        else:
            ok("no Base Protocol sentinel content copied into feature skill")
    else:
        fail(f"base-protocol.md missing: {base_md}")

    finish()


def finish():
    print()
    counts = {"PASS": 0, "WARNING": 0, "FAIL": 0}
    for level, _ in results:
        counts[level] += 1

    for level, message in results:
        print(f"[{level}] {message}")

    print()
    print(f"Summary: {counts['PASS']} PASS, {counts['WARNING']} WARNING, {counts['FAIL']} FAIL")
    if counts["FAIL"] > 0:
        print("RESULT: FAIL")
        sys.exit(1)
    print("RESULT: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
