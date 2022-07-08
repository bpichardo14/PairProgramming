from googleapiclient.discovery import build
import urllib.parse as parse
import pandas as pd
import sqlalchemy as db
import validators

api_key = "AIzaSyDUCymNrzRJbIi2wHCPECwSp3z51LkCVc4"
youtube = build('youtube', 'v3', developerKey=api_key)

# creating the database
engine = db.create_engine('sqlite:///Handbook.db')


# function to retrive the video id
def get_video_id(url):
    """Gets Video-ID from YouTube URL"""

    result = validators.url(url)
    # print(result)
    if result is True:
        url_data = parse.urlparse(url)
        query = parse.parse_qs(url_data.query)
        video_id = query['v'][0]
        return video_id

    else:
        print("Invalid url! Enter a new one: ")
        url_1 = input()
        get_video_id(url_1)


# Function for when the user wants to enter a url
def user_input_video_id():
    youtube_url = input("Please input a YouTube URL: ")
    video_id = get_video_id(youtube_url)

    return video_id


# Function for when the user wants to search videos related to specific topics
def user_input_topic():
    topic = input("Please input the topic you would want to search for: ")
    return topic


# Functions for the user to get videos related to a certain video
def videos_related_to(video_id):
    related_videos = {}

    channel_id = []
    title = []
    description = []
    channel_title = []

    request = youtube.search().list(
        part='snippet',
        maxResults=20,
        relatedToVideoId=video_id,
        type="video"
    )

    response = request.execute()['items']

    for i in range(len(response)):
        channel_id.append(response[i]["snippet"]["channelId"])
        title.append(response[i]["snippet"]["title"])
        description.append((response[i]["snippet"]["description"])[:50])
        channel_title.append(response[i]["snippet"]["channelTitle"])

    related_videos['channelId'] = channel_id
    related_videos['title'] = title
    related_videos['description'] = description
    related_videos['channelTitle'] = channel_title

    return related_videos


# Function to return videos related to a specific topic
def videos_by_search_word(keyword):
    search = keyword
    related_videos = {}

    channel_id = []
    title = []
    description = []
    channel_title = []

    request = youtube.search().list(
        part='snippet',
        maxResults=20,
        q=search
    )

    response = request.execute()['items']

    for i in range(len(response)):
        channel_id.append(response[i]["snippet"]["channelId"])
        title.append(response[i]["snippet"]["title"])
        description.append((response[i]["snippet"]["description"])[:50])
        channel_title.append(response[i]["snippet"]["channelTitle"])

    related_videos['channelId'] = channel_id
    related_videos['title'] = title
    related_videos['description'] = description
    related_videos['channelTitle'] = channel_title

    return related_videos


# Function to get the most PopularVideos
def get_most_popular_videos():
    """Builds a service object and returns the desired data"""
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="US"
    ).execute()

    dictionary = {}
    channel_title = []
    video_title = []
    like_count = []
    view_count = []
    url = []
    # tags = []

    for i in range(len(request['items'])):
        channel_title.append(request['items'][i]['snippet']['channelTitle'])
        video_title.append(request['items'][i]['snippet']['title'])

        like_count.append(request['items'][i]['statistics']['likeCount'])
        view_count.append(request['items'][i]['statistics']['viewCount'])
        url.append('https://www.youtube.com/watch?v=' + request['items'][i]['id'])

    dictionary['channel_title'] = channel_title
    dictionary['video_title'] = video_title
    dictionary['like_count'] = like_count
    dictionary['view_count'] = view_count
    dictionary['url'] = url

    # pprint.pprint(request['items'][0]['id'])

    return dictionary


# Function for creating the dataframe related to videos under a specific topic
def create_topic_dataframe():
    # creating the dataframes
    related_videos = pd.DataFrame.from_dict(videos_by_search_word(user_input_topic()))

    # inserting the following dataframe as a table
    related_videos.to_sql('RelatedVids', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM RelatedVids;").fetchall()
    df = pd.DataFrame(query_result)
    df.columns = ['ChannelId', 'Title', 'Description', 'ChannelTitle']

    return df


def create_popular_dataframe():
    my_dict = get_most_popular_videos()

    popular_videos = pd.DataFrame.from_dict(my_dict)

    popular_videos.to_sql('PopVideos', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM PopVideos;").fetchall()
    table = pd.DataFrame(query_result)
    table.columns = ['channel_title', 'video_title', 'like_count', 'view_count', 'url']

    return table


def create_relate_to_dataframe():
    # creating the dataframes
    related_videos = pd.DataFrame.from_dict(videos_related_to(user_input_video_id()))

    # inserting the following dataframe as a table
    related_videos.to_sql('related_videos', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM related_videos;").fetchall()
    df = pd.DataFrame(query_result)
    df.columns = ['ChannelId', 'Title', 'Description', 'ChannelTitle']

    return df


def instructions():
    head = """

    ----------------------------------------------------------------------i--------------------------------------------------------------------

                                                        📕 WELCOME TO THE CONTENT CREATOR HANDBOOK 📙

                                                            developed by Natasha K. & Brayan P. 

    --------------------------------------------------------------------------------------------------------------------------------------------
    """
    print(head)


if __name__ == "__main__":

    question1 = input("Do you have an idea of what you want to look for? (y/n): ")
    message = "Sorry to see you go! Good bye. Like comment and subscribe ;) "

    if question1 is 'y':
        print(create_topic_dataframe())
    else:
        question2 = input("Do you want to see some popular videos? (y/n): ")
        if question2 is 'y':
            print(create_popular_dataframe())
            question3 = input("Do you want to see more videos related to a specific video? (y/n): ")
            if question3 is 'y':
                print(create_relate_to_dataframe())
                print("Go to the channels listed in the table to learn more about what makes their channels successful!")
                print("Happy Content Creation!")
            else:
                print(message)
        else:
            print(message)
