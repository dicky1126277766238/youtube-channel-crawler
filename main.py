import datetime

from utils.init import init_db

init_db()

from db.models import *
from utils.topic import get_topic_models
from utils.youtube import loop_channel_ids, fetch_channels

# from utils.youtube import init_youtube_client
# init_youtube_client("KEY")

dev = True


def channel_ids_callback(channel_ids):
    items = fetch_channels(channel_ids)
    time_now = datetime.datetime.now()
    for item in items:

        stat = item["statistics"]
        view_count = int(stat["viewCount"])
        subscriber_count = int(stat.get("subscriberCount", 0))
        hidden_subscriber_count = stat["hiddenSubscriberCount"]

        if view_count < 5000 or (not hidden_subscriber_count and subscriber_count < 500):
            continue

        channel_id = item["id"]
        channel, created = Channel.objects.update_or_create(id=channel_id, defaults={
            "title": item["snippet"]["title"],
            "country": item["snippet"].get("country", None),
            "publishedAt": item["snippet"]["publishedAt"],
            "fetched": time_now
        })

        Statistic.objects.update_or_create(id=channel, defaults={
            "viewCount": view_count,
            "subscriberCount": subscriber_count,
            "hiddenSubscriberCount": hidden_subscriber_count,
            "videoCount": int(stat["videoCount"])
        })

        topic_details = item.get("topicDetails", {})
        topics = get_topic_models(topic_details.get("topicIds", []), topic_details.get("topicCategories", []))
        channel.topics.set(topics)

    # terminate loop if return True
    return dev


def main():
    print(f"start: {datetime.datetime.now()}")
    count = loop_channel_ids(channel_ids_callback)
    print(f"{count} channels done")
    print(f"end: {datetime.datetime.now()}")


if __name__ == '__main__':
    main()
