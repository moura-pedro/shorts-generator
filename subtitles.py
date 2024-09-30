import whisper
import subprocess
import os

SUB_OUTPUT_DIR = 'sub_shorts'
INPUT_DIR = 'shorts'

# Load the model
model = whisper.load_model("base")

# Function to convert seconds to SRT time format
def srt_timestamp(seconds):
    import math
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# Transcribe the video
def generate_subtitles(input_path):
    input_video = os.path.join(INPUT_DIR, input_path)
    
    result = model.transcribe(input_video)

    # Ensure the output directory exists
    if not os.path.exists(SUB_OUTPUT_DIR):
        os.makedirs(SUB_OUTPUT_DIR)

    # Write the transcription to an SRT file
    with open(f"{SUB_OUTPUT_DIR}/{input_path}.srt", "w", encoding='utf-8') as srt_file:
        for i, segment in enumerate(result['segments']):
            srt_file.write(f"{i+1}\n")
            start_time = srt_timestamp(segment['start'])
            end_time = srt_timestamp(segment['end'])
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{segment['text'].strip()}\n\n")


def add_subtitles(input_path):

    generate_subtitles(input_path)
    
    input_video = os.path.join(INPUT_DIR, input_path)
    output_video = os.path.join(SUB_OUTPUT_DIR, "sub_" + input_path)
    subtitles = f"{SUB_OUTPUT_DIR}/{input_path}.srt"

    subprocess.call([
        'ffmpeg',
        '-i', input_video,
        '-vf', f"subtitles={subtitles}",
        output_video
    ])

def main():
    add_subtitles("video1-short1.mp4")
    add_subtitles("video1-short2.mp4")
    add_subtitles("video1-short3.mp4")
    add_subtitles("video1-short4.mp4")
    add_subtitles("video1-short5.mp4")

main()
