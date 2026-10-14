# Consolidated Multimedia Analyzer

The capstone command-line tool inspects image, audio, and video metadata and
prints a readable report or JSON.

Run it from the repository root:

```powershell
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/media-file
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/media-file --json
```

Install Python dependencies with:

```powershell
python -m pip install -r Capstone-Projects/Consolidated-Multimedia-Analyzer/requirements.txt
```

Pillow reads image metadata. FFmpeg's `ffprobe` must be installed and available
on `PATH` for audio and video files.