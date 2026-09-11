"""Video metadata analyzer backed by FFprobe."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_probe(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe is not available; install FFmpeg and add it to PATH")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-of", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "FFprobe could not read the video")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("FFprobe returned malformed JSON") from exc


def report(path: Path) -> dict[str, Any]:
    raw = run_probe(path)
    container = raw.get("format", {})
    streams = []
    for stream in raw.get("streams", []):
        kind = stream.get("codec_type", "unknown")
        item: dict[str, Any] = {
            "type": kind,
            "codec": stream.get("codec_long_name") or stream.get("codec_name", "unknown"),
        }
        if kind == "video":
            item.update({
                "resolution": f"{stream.get('width', '?')}x{stream.get('height', '?')}",
                "frame_rate": stream.get("r_frame_rate", "unknown"),
                "pixel_format": stream.get("pix_fmt", "unknown"),
            })
        elif kind == "audio":
            item.update({
                "sample_rate": stream.get("sample_rate", "unknown"),
                "channels": stream.get("channels", "unknown"),
                "layout": stream.get("channel_layout", "unknown"),
            })
        streams.append(item)
    duration = container.get("duration")
    return {
        "file": path.name,
        "format": container.get("format_long_name") or container.get("format_name", "unknown"),
        "size_bytes": path.stat().st_size,
        "duration_seconds": round(float(duration), 2) if duration else None,
        "bitrate": container.get("bit_rate", "unknown"),
        "streams": streams,
        "tags": container.get("tags", {}),
    }


def print_report(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    print("\n" + "=" * 44)
    print("          VIDEO METADATA REPORT")
    print("=" * 44)
    for key, value in data.items():
        if key not in {"streams", "tags"}:
            print(f"{key.replace('_', ' ').title():20}: {value}")
    for title, values in (("STREAMS", data["streams"]), ("TAGS", data["tags"])):
        print(f"\n{title}\n" + "-" * 32)
        if not values:
            print("No data available.")
        elif isinstance(values, list):
            for index, value in enumerate(values, 1):
                print(f"Stream {index}: {value}")
        else:
            for key, value in values.items():
                print(f"{key:<20}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect video and audio streams")
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON output")
    args = parser.parse_args()
    path = args.path or Path(input("Enter video path: ").strip())
    try:
        print_report(report(path), args.json)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
