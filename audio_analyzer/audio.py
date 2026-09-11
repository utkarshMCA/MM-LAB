"""Audio-specific entry point for the Multimedia Lab Toolkit."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from media_lab import ffprobe_report, show  # noqa: E402


if len(sys.argv) != 2:
    print(f"Usage: python {Path(sys.argv[0]).name} AUDIO_FILE")
    raise SystemExit(2)

try:
    show(ffprobe_report(Path(sys.argv[1])), json_mode=False)
except (OSError, RuntimeError, ValueError) as exc:
    print(f"Error: {exc}", file=sys.stderr)
    raise SystemExit(1)
