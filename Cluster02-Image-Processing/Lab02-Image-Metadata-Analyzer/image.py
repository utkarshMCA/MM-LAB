"""Detailed image metadata analyzer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SUPPORTED = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".ppm"}


def size_label(value: int) -> str:
    if value < 1024:
        return f"{value} B"
    if value < 1024**2:
        return f"{value / 1024:.2f} KB"
    return f"{value / 1024**2:.2f} MB"


def collect_metadata(path: Path) -> dict[str, Any]:
    try:
        from PIL import ExifTags, Image
    except ImportError as exc:
        raise RuntimeError("Pillow is missing; install it with: python -m pip install Pillow") from exc

    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"unsupported image format: {path.suffix or 'unknown'}")

    try:
        with Image.open(path) as image:
            exif = {
                ExifTags.TAGS.get(tag, str(tag)): str(value)
                for tag, value in image.getexif().items()
            }
            dpi = image.info.get("dpi")
            return {
                "file": path.name,
                "file_size": size_label(path.stat().st_size),
                "format": image.format or "unknown",
                "width": image.width,
                "height": image.height,
                "aspect_ratio": round(image.width / image.height, 3) if image.height else None,
                "color_mode": image.mode,
                "channels": len(image.getbands()),
                "has_transparency": "A" in image.getbands() or "transparency" in image.info,
                "dpi": dpi or "not recorded",
                "exif": exif,
            }
    except (OSError, ValueError) as exc:
        raise ValueError(f"unable to decode '{path.name}': {exc}") from exc


def print_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print("\n" + "=" * 44)
    print("          IMAGE METADATA REPORT")
    print("=" * 44)
    for key, value in report.items():
        if key not in {"exif"}:
            print(f"{key.replace('_', ' ').title():20}: {value}")
    print("\nEXIF METADATA")
    print("-" * 32)
    if report["exif"]:
        for key, value in report["exif"].items():
            print(f"{key:<20}: {value}")
    else:
        print("No EXIF metadata found.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect image dimensions and metadata")
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON output")
    args = parser.parse_args()
    path = args.path or Path(input("Enter image path: ").strip())
    try:
        print_report(collect_metadata(path), args.json)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
