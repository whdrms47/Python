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
    q="괴물쥐 유튜브",
    order="relevance",
    part="snippet",
    maxResults=10
).execute()

#q채널 재생리스트 정보 불러오기
channel_id = search['items'][0]['snippet']['channelId']
print(channel_id)
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
    video_names.append(PLIN['snippet']['title'])
    video_ids.append(PLIN['snippet']['resourceId']['videoId'])
    date.append(PLIN['snippet']['publishedAt'])

PLIND=pd.DataFrame([date,video_names,video_ids]).T
PLIND.columns=['Date','Title','IDS']
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
PLIND.to_excel('results.xlsx', header=['title', 'category_id', 'views', 'likes', 'comments', 'date'])
print(PLIND)