from celery import shared_task

from forum.models import Tags, Topic, VotedPosts

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

    classifier = pipeline("zero-shot-classification", model="../../models/bart-large-mnli")
    d = classifier(text, labels)

    tagging = [x for x in list(zip(d['labels'], d['scores'])) if x[1] > 0.15]

    for t in tagging:
        tag = Tags(topic=tp, tag_name=t[0], tag_value=t[1])
        tag.save()

    return tagging

@shared_task
def calculate_interests(username):
    interests = {}
    for label in labels:
        interests[label] = 0

    posts = VotedPosts.objects.filter(username=username)

    sum_values = 0 
    for post in posts:
        contains = Tags.objects.filter(topic=post.voted)

        for tag in contains:
            if tag.tag_name in interests:
                interests[tag.tag_name] += tag.tag_value
                sum_values += tag.tag_value


    for k, v in interests.items():
        interests[k] = v / sum_values

    return interests

        
        

