import os
import requests
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&eventType=live&type=video&key={API_KEY}'

# 현재 날짜와 시간을 포맷에 맞게 가져오기
current_date = datetime.now().strftime('%Y-%m-%d')
current_year = datetime.now().strftime('%Y')

markdown_file = f"readme-{current_year}.md"

response = requests.get(URL)
data = response.json()
print(f"data: {data}")

if 'items' in data and len(data['items']) > 0:
    video_id = data['items'][0]['id']['videoId']
    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'
    print(f"live_stream_url: {live_stream_url}")

    if data['items'][0]['snippet']['liveBroadcastContent'] == 'live':
        # readme 파일이 없으면 생성 후 헤더 추가
        if not os.path.exists(markdown_file):
            with open(markdown_file, "w") as f:
                f.write("| Date       | Live Stream URL                                      |\n")
                f.write("|------------|------------------------------------------------------|\n")

        # readme 파일을 읽어서 기존 내용 가져오기
        with open(markdown_file, "r") as f:
            content = f.readlines()

        # 테이블 헤더(상위 2줄)를 유지한 상태에서 새로운 행 추가
        header = content[:2]  # 헤더 2줄 유지
        body = content[2:]  # 기존 내용

        new_entry = f"| {current_date} | [{live_stream_url}]({live_stream_url}) |\n"

        # 중복 체크 (기존 데이터에 이미 있는지 확인)
        if new_entry in body:
            print("Live stream URL already exists for today. Skipping update.")
        else:
            # 최신 라이브 스트림을 테이블의 가장 위에 추가
            with open(markdown_file, "w") as f:
                f.writelines(header + [new_entry] + body)
else:
    print("No live stream currently.")
