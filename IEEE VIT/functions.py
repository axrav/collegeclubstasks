import os

from pytube import YouTube
from youtubesearchpython import VideosSearch


# Functions
def song_url(query: str):
    search = VideosSearch(query, limit=1).result()
    link = search["result"][0]["link"]
    return link


def tube_dl(url: str):
    yt = YouTube(url).streams.filter(only_audio=True).first()
    output = yt.download()
    base, _ = os.path.splitext(output)
    name = base + ".mp3"
    os.rename(output, name)
    return name
