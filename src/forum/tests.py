from django.test import TestCase
from forum.models import Topic, Comment
from datetime import date, timedelta

class TopicTest(TestCase):
    def setUp(self):
        Topic.objects.create(title="title", content="content", pub_date=date.today())

    def test_topic_created(self):
        topic = Topic.objects.get(title="title")

        self.assertEqual(getattr(topic, "content"), "content")

    def test_current_date(self):
        topic = Topic.objects.get(title="title")

        self.assertEqual(date.today(), getattr(topic, "pub_date").date())

class CommentTest(TestCase):
    def setUp(self):
        Topic.objects.create(title="new topic", content="some random description", pub_date=date.today())
        tpc = Topic.objects.get(title="new topic")
        Comment.objects.create(topic=tpc, content="some comment text", votes=5)

    def test_comment_created(self):
        comment = Comment.objects.get(content="some comment text")

        self.assertEqual(getattr(comment, "content"), "some comment text")
        self.assertEqual(getattr(comment, "votes"), 5)
