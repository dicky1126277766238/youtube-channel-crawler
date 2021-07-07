from utils.init import init_db

init_db()

from db.models import TopicCategory

cache = {}


def get_topic_models(topic_ids, topic_categories):
    topics = []
    for topicId, wiki in zip(topic_ids, topic_categories):
        if topicId in cache:
            topics.append(cache[topicId])
        else:
            topic, created = TopicCategory.objects.update_or_create(topicId=topicId, defaults={
                "topicId": topicId,
                "wiki": wiki
            })
            topics.append(topic)
            cache[topicId] = topic
    return topics
