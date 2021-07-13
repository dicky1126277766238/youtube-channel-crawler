import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube_client = None

if "YOUTUBE_API_KEY" in os.environ:
    youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=os.environ["YOUTUBE_API_KEY"])


def init_youtube_client(key):
    global youtube_client
    youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=key)


def loop_channel_ids(callback):
    if youtube_client is None:
        raise Exception("Please init youtube client or set environment variable YOUTUBE_API_KEY")

    count = 0
    search = youtube_client.search()
    request = search.list(
        type='channel',
        part='id',
        maxResults=50
    )

    while request is not None:
        response = request.execute()
        current_items = response.get('items', [])
        count += len(current_items)
        stop = callback([item["id"]["channelId"] for item in current_items])
        if stop:
            break

        request = search.list_next(request, response)

    return count


def fetch_channels(channel_ids):
    if youtube_client is None:
        raise Exception("Please init youtube client or set environment variable YOUTUBE_API_KEY")

    response = youtube_client.channels().list(
        part='snippet,statistics,topicDetails',
        id=','.join(channel_ids),
        maxResults=50
    ).execute()

    return response.get("items", [])


# test
if __name__ == '__main__':
    try:
        loop_channel_ids(fetch_channels)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
