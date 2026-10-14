# Cluster 03: Audio Processing

This cluster contains a Mutagen-based audio metadata analyzer. It reports file
size, duration, bitrate, codec, channel count, sample rate, and embedded tags.

Supported formats include MP3, WAV, FLAC, AAC, M4A, OGG, OGA, and WMA. Install
the project dependencies from the repository root:

```powershell
python -m pip install -r Capstone-Projects/Consolidated-Multimedia-Analyzer/requirements.txt
```

Run the analyzer from the repository root:

```powershell
python Cluster03-Audio-Processing/audio.py path/to/song.mp3
```

If no path is supplied, the program prompts for one. Sample-folder guidance is
in `samples/README.md`; audio files are not committed.
