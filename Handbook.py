from googleapiclient.discovery import build
import urllib.parse as parse
import pdb
import os
import pprint
import pandas as pd
import sqlalchemy as db

api_key = "AIzaSyCCpQY6BJyeA-dO-FIxnMpfRTi9tnkHajE"
youtube = build('youtube', 'v3', developerKey = api_key )

#creating the database
engine = db.create_engine('sqlite:///Handbook.db')

#function to retrive the video id
def get_video_ID(url):
    """Gets Video-ID from YouTube URL"""

    url_data = parse.urlparse(url)
    query = parse.parse_qs(url_data.query)
    video_id = query["v"][0]

    return video_id

#Function for when the user wants to enter a url
def user_input():
    youtube_url = input("Please input a YouTube URL: ")
    video_id = get_video_ID(youtube_url)

    return video_id

#Functions for the user to get videos related to a certain video 
def videos_related_to(video_id):
    relatedVideos = {}

    channelId = []
    title = []
    description = []
    channelTitle = []

    request = youtube.search().list(
        part = 'snippet', 
        maxResults = 20,
        relatedToVideoId = video_id,
        type = "video"
    )

    response = request.execute()['items']

    for i in range(len(response)):
        channelId.append(response[i]["snippet"]["channelId"])
        title.append(response[i]["snippet"]["title"])
        description.append((response[i]["snippet"]["description"])[:50])
        channelTitle.append(response[i]["snippet"]["channelTitle"])

    relatedVideos['channelId'] = channelId
    relatedVideos['title'] = title
    relatedVideos['description'] = description
    relatedVideos['channelTitle'] = channelTitle

    return relatedVideos

#Function to get the most PopularVideos
def get_most_popular_videos():
    """Builds a service object and returns the desired data"""
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="US"
    ).execute()

    dictonary = {}
    channel_title = []
    video_title = []
    like_count = []
    view_count = []
    #tags = []

    for i in range(len(request['items'])):
        channel_title.append(request['items'][i]['snippet']['channelTitle'])
        video_title.append(request['items'][i]['snippet']['title'])

        like_count.append(request['items'][i]['statistics']['likeCount'])
        view_count.append(request['items'][i]['statistics']['viewCount'])

    dictonary['channel_title'] = channel_title
    dictonary['video_title'] = video_title
    dictonary['like_count'] = like_count
    dictonary['view_count'] = view_count
    
    return dictonary


def create_popular_dataframe():
    my_dict = get_most_popular_videos()
    
    PopularVideos = pd.DataFrame.from_dict(my_dict)

    PopularVideos.to_sql('PopVideos', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM PopVideos;").fetchall()
    table = pd.DataFrame(query_result)
    table.columns = ['channel_title', 'video_title', 'like_count', 'view_count']

    return table

def create_relateTo_dataframe():
    #creating the dataframes
    RelatedVideos = pd.DataFrame.from_dict(videos_related_to(user_input()))

    #inserting the following dataframe as a table
    RelatedVideos.to_sql('RelatedVids', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM RelatedVids;").fetchall()
    df = pd.DataFrame(query_result)
    df.columns = ['ChannelId', 'Title', 'Description', 'ChannelTitle']

    return df


if __name__ == "__main__":
    #print(get_most_popular_videos())
    #user_input()
    print(create_popular_dataframe())
    print(create_relateTo_dataframe())

    
