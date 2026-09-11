# Audio Analyzer

This folder contains a complete Mutagen-based audio metadata analyzer.

```powershell
python audio.py path\to\song.mp3
```

If no path is supplied, the program prompts for one. Supported formats are
MP3, WAV, FLAC, AAC, M4A, OGG, OGA, and WMA. Install dependencies from the
project root with `pip install -r requirements.txt`.

The report includes file size, duration, bitrate, codec class, channel count,
sample rate, and embedded tags.
