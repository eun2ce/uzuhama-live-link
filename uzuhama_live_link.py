import os
import requests
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}'

# Markdown 파일 경로
markdown_file = "readme.md"

# 현재 날짜와 시간을 포맷에 맞게 가져오기
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

response = requests.get(URL)
data = response.json()

if 'items' in data and len(data['items']) > 0:
    video_id = data['items'][0]['id']['videoId']
    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'

    if data['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        # readme.md 파일이 없으면 생성 후 읽기
        if not os.path.exists(markdown_file):
            with open(markdown_file, "w") as f:
                f.write("")  # 파일 생성

        # readme.md 파일을 열고 내용을 읽어옴
        with open(markdown_file, "r") as f:
            content = f.readlines()

        # 링크가 이미 존재하는지 확인
        link_found = False
        for i, line in enumerate(content):
            if live_stream_url in line:
                # 이미 존재하는 링크에 시간만 추가
                existing_times = line.split(" ")[0]  # 날짜 부분만 추출
                new_line = f"{existing_times}, {current_time} {live_stream_url}\n"
                content[i] = new_line
                link_found = True
                break

        # 새로운 링크가 없으면 새로운 항목 추가
        if not link_found:
            content.append(f"{current_time} {live_stream_url}\n")

        # 파일에 다시 저장
        with open(markdown_file, "w") as f:
            f.writelines(content)

else:
    print("No live stream currently.")
