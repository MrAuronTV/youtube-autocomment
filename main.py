import os
import pickle
import requests
import json
import time
from urllib import request
from urllib.error import HTTPError
from json import loads
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    channel = 'youtube_channel_id'
    commenttext = 'your_comment'

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json" # your client_secrets_file google console

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    x = 50
    while x < 100:
      try:
       id = pickle.load(open("comment", "rb"))
      except (OSError, IOError) as e:
       foo = 3
       pickle.dump(foo, open("comment", "wb"))
    
      API_ENDPOINT = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=<PLAYLIST ID>&key=<API ACCESS KEY>&maxResults=1'
      r = requests.get(url = API_ENDPOINT)
      video = loads(r.text)['items'][0]['snippet']['resourceId']['videoId']    
      try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "channelId": channel,
                    "videoId": video,
                    "topLevelComment": {
                        "snippet":{
                            "textOriginal": commenttext
                            }
                        }
                    }
                }
        )
        if video:
           if video != id :
               response = request.execute()
               youtube.videos().rate(rating='like', id=video).execute()
               print("http://youtube.com/watch?v={0}".format(video))
        with open('comment', 'wb') as f:
           pickle.dump(video, f)  
      except:
        pass
      #print("Searching video...")
      time.sleep(60)

if __name__ == "__main__":
    main()
