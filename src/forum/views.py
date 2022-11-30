from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime

from .models import Topic, Comment
from .forms import NewTopic, NewComment

def index(request):
    latest_posts = Topic.objects.order_by('-pub_date')[:10]
    context = {
                'latest_posts': latest_posts,
            }

    return render(request, 'forum/index.html', context)

def post(request, post_id):
    post = Topic.objects.get(pk=post_id)
    comments = Comment.objects.all().filter(topic=post)
    context = {
            'post': post,
            'comments': comments,
            } 

    return render(request, 'forum/post.html', context)

def addtopic(request):
    if request.method == 'POST':
        topic = NewTopic(request.POST)

        if topic.is_valid():
            data = topic.cleaned_data

            tp = Topic()
            tp.title = data["title"]
            tp.content = data["content"]
            tp.pub_date = datetime.now().__str__()
            tp.save()

            return HttpResponseRedirect('/forum/')
    else:
        topic = NewTopic()

    return render(request, 'forum/newtopic.html', {'topic': topic})

def comment(request, post_id):
    if request.method == 'POST':
        comment = NewComment(request.POST)

        if comment.is_valid():
            data = comment.cleaned_data
            cm = Comment()

            cm.topic = Topic.objects.get(pk=post_id)
            cm.content = data["content"]
            cm.votes = 0
            cm.pub_date = datetime.now().__str__()
            cm.save()
            
            return HttpResponseRedirect(f"/forum/{post_id}")
    else:
        comment = NewComment()

    return render(request, 'forum/newcomment.html', {'comment': comment, 'post_id': post_id})