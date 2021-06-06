from background_task import background
import requests
from django.conf import settings
from .models import YoutubeFeed


@background()
def youtube_background_calls():

    url = "https://www.googleapis.com/youtube/v3/search/"
    page_token = ""
    params = {
        "key": settings.YOUTUBE_API_KEY,
        "maxResults": settings.MAX_RESULTS,
        "q": 'cricket',
        "pageToken": page_token,
        "part": "snippet"
    }
    response = requests.get(url, params=params)

    saved_video_ids = set()
    youtubefeed_all_instance = YoutubeFeed.objects.all()

    for feed in youtubefeed_all_instance:
        saved_video_ids.add(feed.videoId)

    if response.status_code == 200:
        response_data = response.json()

        for r in response_data['items']:

            if not saved_video_ids or r['id']['videoId'] not in saved_video_ids:
                try:
                    YoutubeFeed_instance = YoutubeFeed.objects.create(
                        title=r['snippet']['title'],
                        description=r['snippet']['description'],
                        published_at=r['snippet']['publishedAt'],
                        thumbnails_URLs=r['snippet']['thumbnails']['default']['url'],
                        videoId=r['id']['videoId']
                    )
                except:
                    print('Failed feed entry, videoId = ', r['id']['videoId'])
    else:
        print('The keys might have expired, replace them with new keys in settings.py file')
        print('status_code = ', response.status_code)
        response_data = response.json()
        if 'error' in response_data and 'message' in response_data['error']:
            print(response_data['error']['message'])
