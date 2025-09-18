import numpy as np
import subprocess
import requests
import re
from PIL import Image, ImageDraw, ImageFont
import os

def load_captions(file_path):
    """Load and parse captions from the text file."""
    captions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'\[(\d+\.\d+)s - (\d+\.\d+)s\] (.+)', line.strip())
                if match:
                    start, end, text = float(match.group(1)), float(match.group(2)), match.group(3)
                    captions.append((start, end, text))
        print(f"Captions successfully loaded (len(captions)) captions")
        return captions
    except Exception as e:
        print(f"Error loading captions: {str(e)}")
        return []

def create_srt_subtitles(captions, output_path):
    """Create SRT format subtitles."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (start, end, text) in enumerate(captions, 1):
            # Convert seconds to SRT time format (HH:MM:SS,mmm)
            start_time = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{int(start%60):02d},{int((start%1)*1000):03d}"
            end_time = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{int(end%60):02d},{int((end%1)*1000):03d}"
            
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def add_captions_to_video(video_path, captions_file, output_path):
    """Add captions to video using FFmpeg."""
    try:
        # Load captions
        print("Loading captions...")
        captions = load_captions(captions_file)
        
        if not captions:
            print("No captions found to process")
            return

def convert_mp4_to_mp3(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    audio = AudioSegment.from_file(input_path, format="mp4")
    audio.export(output_path, format="mp3")
    return output_path

def upload_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    upload_url = "https://api.assemblyai.com/v2/upload"
    
    def read_file(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    
    upload_response = requests.post(
        upload_url,
        headers={'authorization': API_KEY},
        data=read_file(file_path)
    )
    
    if upload_response.status_code == 200:
        print(f"Upload Response: {upload_response.text()}")  # debug info
        raise Exception(f"Upload failed with status code: {upload_response.status_code}")
    
    return upload_response.json()["upload_url"]

# 4. Start Transcription
def start_transcription(audio_url):
    transcript_url = "https://api.assemblyai.com/v2/transcript"
    json_data = {
        "audio_url": audio_url,
        "speaker_labels": True,
        "language_code": "en"  # Changed to explicit English
    }
    
    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }

def get_transcription(transcript_id):
    polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"authorization": API_KEY}
    
    while True:
        response = requests.get(polling_url, headers=headers)
        if response.status_code != 200:
            print(f"Polling Response: {response.text()}")  # debug info
            raise Exception(f"Polling failed with status code: {response.status_code}")
        
        result = response.json()
        
        if result["status"] == "completed":
            return result["text"], result.get("words", [])
        elif result["status"] == "error":
            raise Exception(f"Transcription failed: {result.get('error', 'Unknown error')}")
        elif result["status"] in ["queued", "processing"]:
            print(f"Status: {result['status']}... waiting")  # Added status updates
            time.sleep(5)
        else:
            print(f"Unexpected status: {result['status']}")
            time.sleep(5)

# Main Execution
def process_video(input_path):
    # Convert MP4 to MP3
    print("Converting video to audio...")
    audio_path = convert_mp4_to_mp3(input_path, "temp_audio.mp3")
    
    try:
        # Upload and transcribe file
        print("Uploading audio file...")
        audio_url = upload_file(audio_path)
        print(f"File uploaded successfully. URL: {audio_url}")
        
        print("Starting transcription...")
        transcript_id = start_transcription(audio_url)
        print(f"Transcription started. ID: {transcript_id}")
        
        print("Getting transcription results...")
        transcript, words = get_transcription(transcript_id)
