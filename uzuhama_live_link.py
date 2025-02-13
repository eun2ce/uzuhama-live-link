import os
import requests
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}'

markdown_file = "readme.md"

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

response = requests.get(URL)
data = response.json()

if 'items' in data and len(data['items']) > 0:
    video_id = data['items'][0]['id']['videoId']
    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'

    if data['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        with open(markdown_file, "r") as f:
            content = f.readlines()

        link_found = False
        for i, line in enumerate(content):
            if live_stream_url in line:
                existing_times = line.split(" ")[0]  # 날짜 부분만 추출
                new_line = f"{existing_times}, {current_time} {live_stream_url}\n"
                content[i] = new_line
                link_found = True
                break

        if not link_found:
            content.append(f"{current_time} {live_stream_url}\n")

        # 파일에 다시 저장
        with open(markdown_file, "w") as f:
            f.writelines(content)

else:
    print("No live stream currently.")
