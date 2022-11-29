from django.test import TestCase
from forum.models import Topic, Comment
from datetime import date, timedelta

class TopicTest(TestCase):
    def setUp(self):
        Topic.objects.create(title="title", content="content", pub_date=date.today())

    def test_current_date(self):
        topic = Topic.objects.get(title="title")

        self.assertEqual(getattr(topic, "content"), "content")
        self.assertEqual(date.today(), getattr(topic, "pub_date").date())