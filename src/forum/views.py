from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from django.core.mail import send_mail
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import datetime, date, timedelta

import random

import folium
import streamlit as st
from streamlit_folium import folium_static

import geocoder
from ipware import get_client_ip

from forum.syntheticdata import populate_models
from socialnews.tasks import haversine_distance, classify_text, calculate_interests, predict_user_posts

from .models import Topic, Comment, VotedComments, VotedPosts, Location, UserLocal, Tags
from .forms import NewTopic, NewComment, NewLocation, Distance, SearchBox
from .document import TopicDocument

def index(request):
    user_feed = Topic.objects.order_by('-votes')

    p = Paginator(user_feed, 10)

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

def fakedata(request):
    populate_models()

    messages.add_message(request, messages.INFO, 'Changes applied')

    return render(request, 'forum/messages.html')

def search(request):
    if request.method == "POST":
        searchbox = SearchBox(request.POST)

        if searchbox.is_valid():
            data = searchbox.cleaned_data

            hits = TopicDocument.search().query("multi_match", query=data["query"], fields=["title", "content", "username"])
            results = hits.to_queryset()
        else:
            searchbox = SearchBox()
            results = []
    else:
        searchbox = SearchBox()
        results = []

    return render(request, 'forum/search.html', {'searchbox': searchbox, 'results': results})

def feed(request):
    posts_uuid = predict_user_posts.delay(request.user.get_username()).get()

    user_feed = Topic.objects.filter(uuid__in=posts_uuid)

    p = Paginator(user_feed, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    context = {
                'user_feed': p.page(page_number),
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/feed.html', context)

def newest(request):
    newest_posts = Topic.objects.order_by('-pub_date')

    p = Paginator(newest_posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    context = {
                'user_feed': p.page(page_number),
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
    # Hardcoded IP because in local development there is no public IP available
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

    p = Paginator(local_posts, 10)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    context = {
                'range': range,
                'user_feed': p.page(page_number),
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/local.html', context)

def post(request, post_uuid):
    post = Topic.objects.get(pk=post_uuid)
    comments = Comment.objects.filter(topic=post).order_by('-votes')
    tags = Tags.objects.filter(topic=post)

    p = Paginator(comments, 5)

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
            'tags': tags,
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

    calculate_interests.delay(request.user.get_username())

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
    m = folium.Map()
    m.add_child(folium.LatLngPopup())
    folium_static(m)

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

            text = tp.title + ". " + tp.content

            classify_text.delay(tp.uuid, text)

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

    return render(request, 'forum/newtopic.html', {'topic': topic, 'location': location, 'map': m._repr_html_()})

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
