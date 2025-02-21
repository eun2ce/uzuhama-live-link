import os
import requests
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}'

# Markdown 파일 경로
markdown_file = "readme.md"

# 현재 날짜와 시간을 포맷에 맞게 가져오기
current_date = datetime.now().strftime('%Y-%m-%d')

response = requests.get(URL)
data = response.json()
print(f"data: {data}") 

if 'items' in data and len(data['items']) > 0:
    video_id = data['items'][0]['id']['videoId']
    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'
    print(f"live_strean_url: {live_stream_url}")

    if data['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        # readme.md 파일이 없으면 생성 후 읽기
        if not os.path.exists(markdown_file):
            with open(markdown_file, "w") as f:
                f.write("")  # 파일 생성

        # readme.md 파일을 열고 내용을 읽어옴
        with open(markdown_file, "r") as f:
            content = f.readlines()

        # 기존 날짜에 동일한 URL이 있는지 확인
        for line in content:
            if line.strip() == f"- [{live_stream_url}]({live_stream_url}) - {current_date}":
                print("Live stream URL already exists for today. Skipping update.")
                break
        else:
            # 새로운 항목을 Markdown 리스트 형식으로 추가
            with open(markdown_file, "a") as f:
                f.write(f"- [{live_stream_url}]({live_stream_url}) - {current_date}\n")
else:
    print("No live stream currently.")
