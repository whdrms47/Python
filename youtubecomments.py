from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd

DEVELOPER_KEY = "AIzaSyAp8tyrs0zw9XBHvf9wmYIxxTqlZsodlt0"  # 유튜브 API 키 값
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# build google 객체 생성 (apiclient -> googleapiclient로 수정)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

comments = list()
video_id = '7lxH7xW6CoE'
response = youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id,
    maxResults=10
).execute()
#print(response)

while response:
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append(
            [comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])

    if 'nextPageToken' in response:
        response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id,
                                                 pageToken=response['nextPageToken'], maxResults=10).execute()
    else:
        break
df = pd.DataFrame(comments)
df.to_excel('result.xlsx', header=['comment', 'author', 'date', 'num_likes'], index=None)