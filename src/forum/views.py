from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from django.core.mail import send_mail
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from datetime import datetime

import random

import folium

import geocoder
from ipware import get_client_ip

from elasticsearch import Elasticsearch

from socialnews.tasks import haversine_distance

from .models import Topic, Comment, VotedComments, VotedPosts, Location, UserLocal
from .forms import NewTopic, NewComment, NewLocation, Distance

def index(request):
    latest_posts = Topic.objects.order_by('-pub_date')

    p = Paginator(latest_posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    context = {
                'user_feed': p.page(page_number),
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/index.html', context)

## This view should return posts that match user interests
def feed(request):
    user_feed = Topic.objects.order_by('-votes')

    context = {
                'user_feed': user_feed,
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/feed.html', context)

def newest(request):
    newest_posts = Topic.objects.order_by('-pub_date')

    context = {
                'user_feed': newest_posts,
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/newest.html', context)

def local(request):
    if request.method == 'POST':
        range = Distance(request.POST)

        if range.is_valid():
            data = range.cleaned_data
            distance = 10 * data["range"]
        else:
            range = Distance()
            distance = 1000
    else:
        range = Distance()
        distance = 1000

    posts = Location.objects.select_related('relates')

    ip, is_routable = get_client_ip(request)
    curr = geocoder.ipinfo("31.182.202.212").latlng

    UserLocal.objects.all().delete()

    for post in posts:
        dst = haversine_distance.delay(curr, (post.latitude, post.longitude)).get()

        if dst <= distance:
            local_user_post =  UserLocal.objects.create(topic=Topic.objects.get(pk=post.relates.uuid), username=request.user.get_username(), distance=dst)
            local_user_post.save()

    user_local = UserLocal.objects.prefetch_related('topic').order_by('-distance')
    
    lst = []
    for u in user_local:
        lst.append(u.topic.uuid)

    local_posts = Topic.objects.filter(pk__in=lst)

    context = {
                'range': range,
                'user_feed': local_posts,
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/local.html', context)

def post(request, post_uuid):
    post = Topic.objects.get(pk=post_uuid)
    comments = Comment.objects.filter(topic=post).order_by('-votes')

    p = Paginator(comments, 3)

    if Location.objects.filter(relates=post).exists():
        loc  = Location.objects.get(relates=post).__str__()
    else:
        loc = "Null"

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    context = {
            'post': post,
            'comments': p.page(page_number),
            "loc": loc,
            }

    return render(request, 'forum/post.html', context)

def voteit(request, post_uuid):
    tp = Topic.objects.get(pk=post_uuid)

    try:
        vt = VotedPosts.objects.get(username=request.user.get_username(), voted=tp.uuid)
    except VotedPosts.DoesNotExist:
        tp.votes = tp.votes + 1
        tp.save()

        vt = VotedPosts.objects.create(username=request.user.get_username(), voted=tp.uuid)
        vt.save()

    return HttpResponseRedirect(reverse('forum:index'))

def likeit(request, comment_uuid):
    cm = Comment.objects.get(pk=comment_uuid)
    post_uuid = cm.topic.uuid

    try:
        vt = VotedComments.objects.get(username=request.user.get_username(), voted=cm.uuid)
    except VotedComments.DoesNotExist:
        cm.votes = cm.votes + 1
        cm.save()

        vt = VotedComments.objects.create(username=request.user.get_username(), voted=cm.uuid)
        vt.save()

    return HttpResponseRedirect(reverse('forum:post', args=(post_uuid,)))

@login_required(login_url='/accounts/login/')
def addtopic(request):
    if request.method == 'POST':
        topic = NewTopic(request.POST)

        if topic.is_valid():
            data = topic.cleaned_data
            tp = Topic()
            tp.title = data["title"]
            tp.url = data["url"]
            tp.content = data["content"]
            tp.pub_date = datetime.now().__str__()
            tp.username = request.user.get_username()
            tp.geography = data["location"]
            tp.save()

            if tp.geography:
                location = NewLocation(request.POST)

                if location.is_valid():
                    loc_data = location.cleaned_data

                    loc = Location()
                    loc.relates = tp
                    loc.latitude = loc_data["latitude"]
                    loc.longitude = loc_data["longitude"]
                    loc.save()

                    return HttpResponseRedirect('/forum/')
                else:
                    render(request, 'forum/newtopic.html', {'topic': topic, 'location': location})
            else:
                return HttpResponseRedirect('/forum/')
    else:
        topic = NewTopic()
        location = NewLocation()

    return render(request, 'forum/newtopic.html', {'topic': topic, 'location': location})

@login_required(login_url='/accounts/login/')
def comment(request, post_uuid):
    if request.method == 'POST':
        comment = NewComment(request.POST)

        if comment.is_valid():
            data = comment.cleaned_data
            cm = Comment()

            cm.topic = Topic.objects.get(pk=post_uuid)
            cm.content = data["content"]
            cm.votes = 0
            cm.pub_date = datetime.now().__str__()
            cm.username = request.user.get_username()
            cm.save()

            return HttpResponseRedirect(f"/forum/{post_uuid}")
    else:
        comment = NewComment()

    return render(request, 'forum/newcomment.html', {'comment': comment, 'post_uuid': post_uuid})
