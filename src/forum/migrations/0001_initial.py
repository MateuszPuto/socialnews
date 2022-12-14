# Generated by Django 4.1.3 on 2022-12-13 13:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Secrets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50)),
                ("secret", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("url", models.URLField()),
                ("content", models.CharField(max_length=500)),
                ("pub_date", models.DateTimeField(verbose_name="publish date")),
                ("votes", models.IntegerField(default=0)),
                ("username", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="VotedComments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50)),
                ("voted", models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name="VotedPosts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=50)),
                ("voted", models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.CharField(max_length=200)),
                ("votes", models.IntegerField(default=0)),
                ("username", models.CharField(max_length=50)),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forum.topic"
                    ),
                ),
            ],
        ),
    ]
