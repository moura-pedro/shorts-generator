import yt_dlp
import subprocess
import os

OUTPUT_DIR = 'shorts'  # Replace with your desired directory path

def make_shorts(video, num_short):
    url = video.url
    shorts_timestamps = video.get_shorts()

    for i in range(len(shorts_timestamps)):
        start, end = shorts_timestamps[i]
        download_short(url, start, end, f"video{num_short}-short{i+1}.mp4")


def download_short(url, start, end, name):
    filename = name
    target = os.path.join(OUTPUT_DIR, filename)

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
        result = ydl.extract_info(url, download=False)
        short = result['entries'][0] if 'entries' in result else result

    short_url = short['url']

    # Use FFmpeg to process the video
    subprocess.call([
        'ffmpeg', '-i', short_url, '-ss', start, '-to', end, '-c:v', 'copy', '-c:a', 'copy', target
    ])

