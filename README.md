# Multimedia Systems Lab

An independently implemented collection of multimedia lab work. The current
image, audio, and video analyzers inspect media metadata from the command line.

## Student Information

| Field | Details |
| --- | --- |
| Name | Utkarsh Tiwari |
| Roll number | IC-2K22-94 |

## Implemented Work

- Image analysis: format, dimensions, color mode, DPI, file size, and EXIF.
- Audio analysis: codec, sample rate, channels, duration, and embedded tags.
- Video analysis: codecs, resolution, frame rate, pixel format, duration, and tags.
- A unified CLI that prints readable reports or JSON and can save JSON reports to a chosen path.

Images use Pillow, audio tags use Mutagen, and the unified audio/video probe
uses FFprobe from FFmpeg. The other clusters are present as coursework folders
and are marked individually until implementations are added.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r Capstone-Projects/Consolidated-Multimedia-Analyzer/requirements.txt
```

Install FFmpeg and make sure `ffprobe` is on `PATH` for unified audio and video
inspection.

## Usage

Run the unified analyzer from the repository root:

```powershell
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/photo.jpg
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/recording.mp3
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/clip.mp4 --json
python Capstone-Projects/Consolidated-Multimedia-Analyzer/media_lab.py path/to/clip.mp4 --output reports/clip.json
```

Individual lab entry points:

```powershell
python Cluster02-Image-Processing/Lab02-Image-Metadata-Analyzer/image.py path/to/photo.jpg --json
python Cluster03-Audio-Processing/audio.py path/to/recording.mp3 --json
python Cluster04-Video-Processing/Lab03-Video-Metadata-Analyzer/video.py path/to/clip.mp4 --json
```

## Repository Structure

```text
.
|-- Capstone-Projects/Consolidated-Multimedia-Analyzer/
|   |-- media_lab.py
|   `-- requirements.txt
|-- Cluster01-Multimedia-Fundamentals/
|-- Cluster02-Image-Processing/Lab02-Image-Metadata-Analyzer/
|-- Cluster03-Audio-Processing/
|-- Cluster04-Video-Processing/Lab03-Video-Metadata-Analyzer/
|-- Cluster05-Compression/
|-- Cluster06-Multimedia-Communication/
|-- Cluster07-Interactive-Multimedia/
|-- Cluster08-Advanced-Multimedia-AI/
|-- datasets/
`-- docs/
```

See each cluster README for its current implementation status.

