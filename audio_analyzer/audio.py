"""Inspect audio properties and embedded tags using Mutagen."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from mutagen import File

SUPPORTED_FORMATS = {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".wma"}


def format_size(byte_count: int) -> str:
    if byte_count < 1024:
        return f"{byte_count} B"
    if byte_count < 1024**2:
        return f"{byte_count / 1024:.2f} KB"
    return f"{byte_count / 1024**2:.2f} MB"


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "Not available"
    total = max(0, int(round(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, seconds_part = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d}"


def read_audio(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        choices = ", ".join(sorted(SUPPORTED_FORMATS))
        raise ValueError(f"unsupported format '{path.suffix or 'unknown'}'; use {choices}")

    audio = File(path)
    if audio is None or audio.info is None:
        raise ValueError("Mutagen could not read this audio file")

    info = audio.info
    bitrate = getattr(info, "bitrate", None)
    tags = {str(key): str(value) for key, value in (audio.tags or {}).items()}
    sample_rate = getattr(info, "sample_rate", None)
    return {
        "file_name": path.name,
        "file_size": format_size(os.path.getsize(path)),
        "format": path.suffix.lower().lstrip("."),
        "duration": format_duration(getattr(info, "length", None)),
        "bitrate": f"{bitrate / 1000:.0f} kbps" if bitrate else "Not available",
        "channels": getattr(info, "channels", "Not available"),
        "sample_rate": f"{sample_rate} Hz" if sample_rate else "Not available",
        "codec": type(info).__name__,
        "tags": tags,
    }


def print_report(report: dict[str, Any]) -> None:
    print("\n" + "=" * 42)
    print("       AUDIO METADATA REPORT")
    print("=" * 42)
    print(f"File Name       : {report['file_name']}")
    print(f"File Size       : {report['file_size']}")
    print(f"File Format     : {report['format'].upper()}")
    print("\nAUDIO\n" + "-" * 32)
    print(f"Duration        : {report['duration']}")
    print(f"Bit Rate        : {report['bitrate']}")
    print(f"Codec           : {report['codec']}")
    print(f"Channels        : {report['channels']}")
    print(f"Sampling Rate   : {report['sample_rate']}")
    print("\nMETADATA\n" + "-" * 32)
    if report["tags"]:
        for key, value in report["tags"].items():
            print(f"{key:<18}: {value}")
    else:
        print("No metadata available.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze audio metadata with Mutagen")
    parser.add_argument("path", nargs="?", type=Path, help="audio file to inspect")
    args = parser.parse_args()
    path = args.path or Path(input("Enter audio path: ").strip())
    try:
        print_report(read_audio(path))
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
