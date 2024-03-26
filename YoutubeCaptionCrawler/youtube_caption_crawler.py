import requests
import json
import os
from multiprocessing import Process
from google.oauth2.service_account import Credentials
import google.auth.transport.requests
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import youtube_dl

YOUTUBE_API_KEY = 'AIzaSyDldj-C2kEAfAsbnGO_eodXMmE8nOWUkJk'
YOUTUBE = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def _make_captions_folder_if_needed(folder_name):
    new_folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

def _get_playlist_video_ids(playlist_id):
    response = YOUTUBE.playlists().list(
        part='snippet',
        id=playlist_id
    ).execute()

    playlist_title = response['items'][0]['snippet']['title']

    # 建立請求並取得回應
    request = YOUTUBE.playlistItems().list(
        part='snippet',
        maxResults=50, # 最多可以取得50個影片資訊，若播放列表超過50部影片，需要使用換頁功能(page token)
        playlistId=playlist_id
    )
    response = request.execute()

    # 從回應中提取影片ID
    video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
    print(video_ids)
    return (video_ids, playlist_title)

def _get_video_caption(video_id, save_folder_path):    
    request = YOUTUBE.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    video_title = response["items"][0]["snippet"]["title"]
    file_path = os.path.join(save_folder_path, video_title)
    print(file_path)
    options = {
        'writesubtitles': True,  # 告訴 youtube_dl 要下載字幕
        'writeautomaticsub': True,  # 告訴 youtube_dl 要下載自動生成的字幕
        'subtitleslangs': ['en'],  # 指定要下載的字幕語言
        'subtitlesformat': 'srt',  # 指定要下載的字幕格式
        'outtmpl': file_path,  # 設定輸出的檔案路徑和檔名格式
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + video_id])

def download_playlist_videos_captions(playlist_id):
    (video_ids, playlist_title) = _get_playlist_video_ids(playlist_id)
    _make_captions_folder_if_needed(playlist_title)
    saved_folder_path = os.path.join(os.getcwd(), playlist_title)
    processes = []
    for video_id in video_ids:
        _get_video_caption(video_id, saved_folder_path)
    #     p = Process(target=_get_video_caption, args=(video_id, saved_folder_path,))
    #     p.start()
    #     processes.append(p)
    # for p in processes:
    #     p.join()

    


