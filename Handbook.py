from googleapiclient.discovery import build
import urllib.parse as parse
import pdb
import os


def get_video_ID(url):
    """Gets Video-ID from YouTube URL"""

    url_data = parse.urlparse(url)
    query = parse.parse_qs(url_data.query)
    video_id = query["v"][0]

    return video_id


def get_request(video_id):
    """Builds a service object and returns the desired data"""

    youtube = build('youtube', 'v3', id = "Your_API_Key" )
    request = youtube.videos().getRating(id = vid_id) 
    data = request.execute()['items']

    return data

if __name__ == "__main__":
    youtube_url = input("Please input a YouTube URL: ")

    vid_id = get_video_ID(youtube_url)
    response = get_request(vid_id)

    
    print(response)

