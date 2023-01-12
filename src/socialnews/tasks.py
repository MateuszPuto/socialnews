from celery import shared_task

from forum.models import Tags, Topic, VotedPosts, About, Interest

labels = ["celebrity", "news", "science", "opinion", "sports", "fashion", "technology", "medical", "politics", "art"]

@shared_task
def haversine_distance(point, point2):
    import math
    '''Used to calculate distance between two polar coordinate points on a sphere'''
    lat, long = point
    lat2, long2 = point2

    lat = math.radians(lat)
    long = math.radians(long)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    a = math.pow(math.sin(abs(lat - lat2)) / 2, 2) + math.cos(lat) * math.cos(lat2) *  math.pow(math.sin(abs(long - long2)) / 2, 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    
    return R * c

@shared_task
def classify_text(tp, text):
    from transformers import pipeline

    topic = Topic.objects.get(uuid=tp)

    classifier = pipeline("zero-shot-classification", model="../../models/bart-large-mnli")
    d = classifier(text, labels)

    tagging = [x for x in list(zip(d['labels'], d['scores'])) if x[1] > 0.15]

    for t in tagging:
        tag = Tags(topic=topic, tag_name=t[0], tag_value=t[1])
        tag.save()

    about = About(topic=topic, vals=list(d['scores']))
    about.save()

    return list(d['scores'])

@shared_task
def calculate_interests(username):
    from collections import OrderedDict

    interests = OrderedDict()
    for label in labels:
        interests[label] = 0

    posts = VotedPosts.objects.filter(username=username)

    total = 0
    for post in posts:
        contains = Tags.objects.filter(topic=Topic.objects.get(uuid=post.voted))

        for tag in contains:
            if tag.tag_name in interests:
                interests[tag.tag_name] += tag.tag_value
                total += tag.tag_value

    if total > 0:
        for key, value in interests.items():
            interests[key] = value / total

    prev_i = Interest.objects.filter(username=username)
    for i in prev_i:
        i.delete()

    i = Interest(username=username, vals=list(interests.values()))
    i.save()

    return interests


@shared_task
def predict_user_posts(username):
    from sklearn.cluster import KMeans
    import numpy as np
    from datetime import date, timedelta

    now = date.today()
    week_before = now - timedelta(days=7)

    posts = Topic.objects.all()

    posts_class = []
    for post in posts:
        posts_class.append(About.objects.get(topic=post).vals)

    datapoints = np.array(posts_class)
    kmeans = KMeans().fit(datapoints)

    interests = [Interest.objects.get(username=username).vals]
    classification = kmeans.predict(interests)

    predicted_posts = []
    for i, label in enumerate(kmeans.labels_):
        if label == classification[0]:
            predicted_posts.append(posts[i].uuid)

    return predicted_posts
        

