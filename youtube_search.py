from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import config


DEVELOPER_KEY = config.DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = config.YOUTUBE_API_SERVICE_NAME
YOUTUBE_API_VERSION = config.YOUTUBE_API_VERSION

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=options,
      part="id,snippet",
      #maxResults=options.max_results
      maxResults=10
    ).execute()

    unsorted_videos = []
    loop_video = []
    video_list_final = []

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        loop_video.append(search_result["snippet"]["title"])
        loop_video.append(search_result["id"]["videoId"])

        unsorted_videos.append(loop_video)
        loop_video = []

    for video in unsorted_videos:
        temp_video = { }
        temp_video['title'] = video[0]
        temp_video['link'] = video[1]
        video_list_final.append(temp_video)

    return video_list_final


def convert_youtube_results(search_query):
    youtube_videos = youtube_search(search_query)
    youtube_videos_json = json.dumps(youtube_videos)
    youtube_videos_list = json.loads(youtube_videos_json)

    return youtube_videos_list


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))