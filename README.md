# Multimedia Lab Toolkit

A clean-room multimedia metadata project for a multimedia laboratory task.
It inspects images with Pillow and audio/video files with FFprobe, then prints
either a readable report or JSON.

## Run

```powershell
pip install -r requirements.txt
python media_lab.py photo.jpg
python media_lab.py movie.mp4 --json
```

FFmpeg must be installed and `ffprobe` must be available on `PATH` for audio
and video files. Pillow is used for image metadata and EXIF tags.

## Features

- image format, dimensions, color mode, DPI, and EXIF data;
- audio codec, sample rate, channels, duration, and tags;
- video dimensions, frame rate, codecs, duration, and tags;
- readable terminal output and machine-readable JSON;
- clear errors for missing files and unavailable tools.

## Folder layout

- `audio_analyzer/audio.py` — audio-only entry point
- `image_analyzer/image.py` — image-only entry point
- `video_analyzer/video.py` — video-only entry point
- `media_lab.py` — shared implementation and unified CLI

## Author

Utkarsh Tiwari
