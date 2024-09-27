from googleapiclient.discovery import build
import re
from collections import Counter
from video import Video


# YTv3 API key
from secret_key import API_KEY

YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

def create_request(region, num_of_videos):
    # Create a request to get the most popular videos
    request = YOUTUBE.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        regionCode=region,              # Region
        maxResults=num_of_videos,        # Number of videos to retrieve
    )
    return request


def get_videos(request):
    response = request.execute()
    videos = []

    # Parse and display the results
    for item in response['items']:
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        date = item['snippet']['publishedAt']
        views = item['statistics']['viewCount']
        video_id = item['id']

        video = Video(title, channel, date, views, video_id)
        videos.append(video)
    
    return videos


def find_comments(id):
    comments = []
    next_page_token = None

    while True:
        request = YOUTUBE.commentThreads().list(
            part='snippet',
            videoId=id,
            pageToken=next_page_token,
            maxResults=100
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return comments


def get_timestamps(comments):
    # Find timestamps in comments
    timestamps = []
    timestamp_pattern = r'\b(\d{1,2}:\d{2})\b'

    for comment in comments:
        matches = re.findall(timestamp_pattern, comment)
        timestamps.extend(matches)

    # Count occurrences of each timestamp
    timestamp_counts = Counter(timestamps)

    # Display most mentioned timestamps
    most_common = timestamp_counts.most_common(5)
    return most_common
