from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def loop_channel_ids(callback):
    count = 0
    search = youtube.search()
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
    response = youtube.channels().list(
        part='snippet,statistics,topicDetails',
        id=','.join(channel_ids),
        maxResults=50
    ).execute()

    return response.get("items", [])


if __name__ == '__main__':
    try:
        loop_channel_ids(fetch_channels)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
