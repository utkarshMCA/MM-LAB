"""Multimedia Lab Toolkit: inspect image, audio, and video metadata."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".ppm"}
AUDIO_TYPES = {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".wma", ".opus"}
VIDEO_TYPES = {".mp4", ".avi", ".mkv", ".mov", ".webm", ".wmv", ".flv", ".m4v", ".mpeg", ".mpg", ".3gp"}


def size_text(number: int) -> str:
    value = float(number)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{number} B"


def image_report(file_path: Path) -> dict[str, Any]:
    try:
        from PIL import ExifTags, Image
    except ImportError as exc:
        raise RuntimeError("Pillow is missing; install it with: python -m pip install Pillow") from exc

    try:
        with Image.open(file_path) as image:
            exif = {
                ExifTags.TAGS.get(tag, str(tag)): str(value)
                for tag, value in image.getexif().items()
            }
            return {
                "type": "image",
                "file": file_path.name,
                "file_size": size_text(file_path.stat().st_size),
                "format": image.format or "unknown",
                "width": image.width,
                "height": image.height,
                "color_mode": image.mode,
                "dpi": image.info.get("dpi", "not recorded"),
                "exif": exif,
            }
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read image '{file_path.name}': {exc}") from exc


def ffprobe_report(file_path: Path, media_type: str) -> dict[str, Any]:
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe is not installed or is not available on PATH")
    command = [
        "ffprobe", "-v", "error", "-of", "json",
        "-show_format", "-show_streams", str(file_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "ffprobe rejected this file")
    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("ffprobe returned invalid JSON") from exc

    if not any(stream.get("codec_type") == media_type for stream in raw.get("streams", [])):
        article = "an" if media_type == "audio" else "a"
        raise ValueError(f"file does not contain {article} {media_type} stream")

    streams = []
    for stream in raw.get("streams", []):
        entry: dict[str, Any] = {
            "kind": stream.get("codec_type", "unknown"),
            "codec": stream.get("codec_long_name") or stream.get("codec_name", "unknown"),
        }
        if stream.get("codec_type") == "video":
            entry.update({
                "resolution": f"{stream.get('width', '?')}x{stream.get('height', '?')}",
                "frame_rate": stream.get("r_frame_rate", "unknown"),
                "pixel_format": stream.get("pix_fmt", "unknown"),
            })
        elif stream.get("codec_type") == "audio":
            entry.update({
                "sample_rate": stream.get("sample_rate", "unknown"),
                "channels": stream.get("channels", "unknown"),
                "channel_layout": stream.get("channel_layout", "unknown"),
            })
        streams.append(entry)

    details = raw.get("format", {})
    duration = details.get("duration")
    return {
        "type": media_type,
        "file": file_path.name,
        "file_size": size_text(file_path.stat().st_size),
        "container": details.get("format_long_name") or details.get("format_name", "unknown"),
        "duration_seconds": round(float(duration), 2) if duration else None,
        "bit_rate": details.get("bit_rate", "unknown"),
        "streams": streams,
        "tags": details.get("tags", {}),
    }


def inspect(file_path: Path) -> dict[str, Any]:
    if not file_path.is_file():
        raise FileNotFoundError(f"file not found: {file_path}")
    extension = file_path.suffix.lower()
    if extension in IMAGE_TYPES:
        return image_report(file_path)
    if extension in AUDIO_TYPES:
        return ffprobe_report(file_path, "audio")
    if extension in VIDEO_TYPES:
        return ffprobe_report(file_path, "video")
    supported = ", ".join(sorted(IMAGE_TYPES | AUDIO_TYPES | VIDEO_TYPES))
    raise ValueError(f"unsupported media type '{extension or 'no extension'}'; supported extensions: {supported}")


def show(report: dict[str, Any], json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(f"{report['type'].upper()} METADATA\n" + "-" * 48)
    for key, value in report.items():
        if key not in {"type", "file", "streams", "exif", "tags"}:
            print(f"{key.replace('_', ' ').title():18}: {value}")
    for name in ("streams", "exif", "tags"):
        values = report.get(name)
        if not values:
            continue
        print(f"\n{name.title()}")
        if isinstance(values, list):
            for item in values:
                print(f"  {item}")
        else:
            for key, value in values.items():
                print(f"  {key}: {value}")


def save_json(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Read metadata from multimedia files")
    parser.add_argument("file", type=Path, help="path to an image, audio, or video file")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    parser.add_argument("--output", type=Path, metavar="JSON_PATH", help="save a JSON report to this path")
    args = parser.parse_args()
    try:
        report = inspect(args.file)
        if args.output is not None:
            if args.output.resolve() == args.file.resolve():
                raise ValueError("JSON output path must differ from the input file")
            save_json(report, args.output)
        show(report, args.json)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
