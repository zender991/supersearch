from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCjdP4tZZh3eUc_wgxXX6hjdct-mo0Gp34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    search_response = youtube.search().list(
      q=options,
      part="id,snippet",
      #maxResults=options.max_results
      maxResults=5
    ).execute()

#########-----------------------------------------------------
    print (search_response)
    videos = []
    #videos = {}
    channels = []
    playlists = []
    links = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append("Title: %s , link: https://www.youtube.com/watch?v=%s" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))

      #if search_result["id"]["kind"] == "youtube#video":
        #videos['title'] = search_result["snippet"]["title"]
        #videos['link'] = search_result["id"]["videoId"]
        #videos.append("Title: %s , link: https://www.youtube.com/watch?v=%s" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))

      #elif search_result["id"]["kind"] == "youtube#channel":
        #channels.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["channelId"]))

      #elif search_result["id"]["kind"] == "youtube#playlist":
        #playlists.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["playlistId"]))
    #print(videos)
    #print (videos)


    #print ("Videos:\n", "\n".join(videos), "\n")

    #return videos
    print(search_response.__class__)
    return search_response
    #print ("Channels:\n", "\n".join(channels), "\n")
    #print ("Playlists:\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        #print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


#que = "Common WHO Questions in English"
#youtube_search(options={"mettalica"})
#search_query = input('Enter keywords: - ')

youtube_search("bon jovi")

