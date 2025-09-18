Video-to-Text Transcription Tool
A Python-based video processing tool that automatically converts MP4 videos to audio and generates accurate transcriptions using AssemblyAI's speech-to-text API.
Features

Video to Audio Conversion: Seamlessly converts MP4 video files to MP3 audio format
Automatic Transcription: Uses AssemblyAI API for high-quality speech-to-text conversion
Speaker Detection: Identifies and labels different speakers in multi-speaker content
SRT Subtitle Generation: Creates industry-standard SRT subtitle files with timestamps
Caption Processing: Loads and processes existing caption files for video overlays
Real-time Status Updates: Monitors transcription progress with polling mechanism

Requirements

Python 3.7+
AssemblyAI API key
Required packages:

pydub - Audio processing
requests - HTTP requests
Pillow (PIL) - Image processing for captions
numpy - Numerical operations
subprocess - System process management



Installation

Clone this repository:

bashgit clone https://github.com/yourusername/video-transcription-tool.git
cd video-transcription-tool

Install required dependencies:

bashpip install pydub requests Pillow numpy

Set up your AssemblyAI API key:

Sign up at AssemblyAI
Get your API key from the dashboard
Add it to the script: API_KEY = "your_api_key_here"



Usage
python# Process a video file
input_video = "your_video.mp4"
process_video(input_video)
The script will:

Convert your MP4 video to MP3 audio
Upload the audio to AssemblyAI
Start the transcription process
Poll for completion and retrieve results
Generate timestamped transcriptions and SRT files

File Structure

video_transcription.py - Main processing script
Generated outputs:

temp_audio.mp3 - Extracted audio file
captions.srt - SRT subtitle file
Transcription text with timestamps



Configuration
The tool supports various transcription settings:

Language Detection: Automatic or specify language code
Speaker Labels: Enable/disable speaker identification
Custom Formatting: Modify timestamp and caption formats

Error Handling
Robust error handling for:

File not found errors
API request failures
Network connectivity issues
Invalid audio formats
Transcription processing errors

Contributing

Fork the repository
Create a feature branch (git checkout -b feature/new-feature)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature/new-feature)
Create a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

AssemblyAI for providing the speech-to-text API
PyDub for audio processing capabilities
