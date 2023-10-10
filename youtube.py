from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import re

DEVELOPER_KEY = "AIzaSyAp8tyrs0zw9XBHvf9wmYIxxTqlZsodlt0"  # 유튜브 API 키 값
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# build google 객체 생성 (apiclient -> googleapiclient로 수정)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#q에 해당하는 채널 정보 불러오기
search = youtube.search().list(
    q="빠더너스 BDNS",
    order="relevance",
    part="snippet",
    maxResults=10
).execute()

#q채널 재생리스트 정보 불러오기
channel_id = search['items'][0]['snippet']['channelId']
#UCDBAVzfX3yZ1hah0FHnOoaA
playlists=youtube.playlists().list(
    channelId= channel_id,
    part = "snippet",
    maxResults=10
).execute()

#q채널 재생리스트 정보 DateFrame으로 정리
playlist_titles=[]
playlist_ids=[]
for PL in playlists['items']:
    playlist_titles.append(PL['snippet']['title'])
    playlist_ids.append(PL['id'])

PLD = pd.DataFrame([playlist_ids,playlist_titles]).T
PLD.columns=['PlayLists','Titles']

#DateFrame으로 정리한 플레이리스트 중 N번째에 해당하는 정보 불러오기
PLI = PLD['PlayLists'][2]
video = youtube.playlistItems().list(
    playlistId = PLI,
    part = 'snippet',
    maxResults = 10,
)
video_list = video.execute()
video_names = []
video_ids = []
date = []
category_id = []

for PLIN in video_list['items']:
    video_ids.append(PLIN['snippet']['resourceId']['videoId'])
PLIND=pd.DataFrame([video_ids]).T
PLIND.columns=['IDS']
print(PLIND)

title = []
category_id = []
views = []
likes = []
comments=[]
date = []
for PJG in range(len(PLIND)):
    request = youtube.videos().list(
    part='snippet,statistics',
    id=PLIND['IDS'][PJG])
    response = request.execute()
    title.append(response['items'][0]['snippet']['title'])
    category_id.append(response['items'][0]['snippet']['categoryId'])
    views.append(response['items'][0]['statistics']['viewCount'])
    likes.append(response['items'][0]['statistics']['likeCount'])
    comments.append(response['items'][0]['statistics']['commentCount'])
    date.append(response['items'][0]['snippet']['publishedAt'])

PLIND=pd.DataFrame([title, category_id, views, likes, comments, date]).T
PLIND.columns=['제목','카테고리','조회수','좋아요','댓글 수','날짜']
# PLIND.to_excel('results.xlsx', header=['title', 'category_id', 'views', 'likes', 'comments', 'date'])
print(PLIND)

#코멘트 저장
comments = list()
video_id = 'W8pxyQT5cRY'
response = youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id,
    maxResults=10
).execute()
print(response)

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

xlxs_dir = 'PJG.xlsx' #경로 및 파일명 설정

with pd.ExcelWriter(xlxs_dir) as writer:

    PLIND.to_excel(writer, sheet_name = '좋아요', header=['제목', '카테고리ID', '조회수', '좋아요', '댓글 수', '날짜'], index=None) #raw_data1 시트에 저장
    df.to_excel(writer, sheet_name = '댓글', header=['텍스트', '작성자', '날짜', '좋아요'], index=None)
