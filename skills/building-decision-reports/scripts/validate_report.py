#!/usr/bin/env python3
"""Validate local image references and basic SVG accessibility in a Markdown report."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((<[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")


def local_target(raw_target: str) -> str | None:
    target = raw_target[1:-1] if raw_target.startswith("<") else raw_target
    target = unquote(target.split("#", 1)[0])
    if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    return target


def validate_svg(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"{path}: invalid SVG XML: {exc}"]

    children = {child.tag.rsplit("}", 1)[-1]: child for child in root}
    for required in ("title", "desc"):
        element = children.get(required)
        if element is None or not "".join(element.itertext()).strip():
            errors.append(f"{path}: SVG needs a non-empty <{required}>")

    if not root.attrib.get("viewBox"):
        errors.append(f"{path}: SVG needs a viewBox")
    if root.attrib.get("role") != "img":
        errors.append(f"{path}: SVG root needs role=\"img\"")
    if not root.attrib.get("aria-labelledby"):
        errors.append(f"{path}: SVG root needs aria-labelledby")
    return errors


def validate_fences(text: str, report: Path) -> list[str]:
    errors: list[str] = []
    marker: str | None = None
    length = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not match:
            continue
        fence_text = match.group(1)
        if marker is None:
            marker, length = fence_text[0], len(fence_text)
        elif fence_text[0] == marker and len(fence_text) >= length:
            marker, length = None, 0
    if marker is not None:
        errors.append(f"{report}: unclosed Markdown code fence")
    return errors


def validate_report(report: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    text = report.read_text(encoding="utf-8")
    errors.extend(validate_fences(text, report))

    image_count = 0
    for alt, raw_target in IMAGE_RE.findall(text):
        image_count += 1
        if not alt.strip():
            errors.append(f"{report}: image {raw_target} has empty alt text")
        target = local_target(raw_target)
        if target is None:
            continue
        image_path = (report.parent / target).resolve()
        if not image_path.is_file():
            errors.append(f"{report}: missing image {target}")
            continue
        if image_path.suffix.lower() == ".svg":
            errors.extend(validate_svg(image_path))

    if "xychart-beta" in text:
        warnings.append(
            f"{report}: Mermaid xychart detected; render and inspect its labels and legend carefully"
        )
    if image_count == 0:
        warnings.append(f"{report}: no Markdown images found")
    return errors, warnings, image_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Markdown report to validate")
    args = parser.parse_args()
    report = args.report.expanduser().resolve()

    if not report.is_file():
        print(f"ERROR: report not found: {report}", file=sys.stderr)
        return 2
    if report.suffix.lower() not in {".md", ".markdown"}:
        print(f"ERROR: expected a Markdown report: {report}", file=sys.stderr)
        return 2

    errors, warnings, image_count = validate_report(report)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"OK: {report} ({image_count} image(s), {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
