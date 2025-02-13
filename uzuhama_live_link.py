import os
import requests
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}'

# Markdown 파일 경로
markdown_file = "readme.md"

response = requests.get(URL)
data = response.json()

if 'items' in data and len(data['items']) > 0:
    video_id = data['items'][0]['id']['videoId']
    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'

    if data['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(markdown_file, "a") as f:
            f.write(f"- {current_datetime} [live_stream_url]({live_stream_url})\n")
else:
    print("No live stream currently.")
