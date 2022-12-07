from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import Topic, Comment, VotedComments
from .forms import NewTopic, NewComment, CreateAccount, CheckPassword

def index(request):
    latest_posts = Topic.objects.order_by('-pub_date')[:10]
    context = {
                'latest_posts': latest_posts,
            }

    if request.user.is_authenticated:
        context["user"] = request.user.get_username()

    return render(request, 'forum/index.html', context)

def create_account(request):
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data["password"] != data["confirm_password"]:
                raise Http404("Password needs to be identical.")

            new_user = User.objects.create_user(data["username"], email=data["email"], password=data["password"])
            new_user.first_name = data["first_name"]
            new_user.last_name = data["last_name"]
            new_user.save()

            return HttpResponse(f'Thanks {data["username"]} for registering on your site.')
    else:
        form = CreateAccount()

    return render(request, 'forum/register.html', {'form': form})

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.user.is_authenticated:
        context = {}
        context["username"] = request.user.get_username()
        context["fullname"] = request.user.get_full_name()
        context["email"] = request.user.email
        context["password"] = ""

        return render(request, 'forum/profile.html', context)
    else:
        return HttpResponse("Something went wrong.")

@login_required(login_url='/accounts/login/')
def check_password_if_valid(request):
    user = request.user

    if request.method == 'POST':
        form = CheckPassword(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if user.check_password(raw_password=data["password"]):
              return HttpResponse("This is valid password.")
            else:
                return HttpResponse("This is not a valid password.")
    else:
        form = CheckPassword()

    return render(request, 'forum/checkpassword.html', {'form': form})

def post(request, post_uuid):
    post = Topic.objects.get(pk=post_uuid)
    comments = Comment.objects.all().filter(topic=post)
    context = {
            'post': post,
            'comments': comments,
            } 

    return render(request, 'forum/post.html', context)

def likeit(request, comment_uuid):
    cm = Comment.objects.get(pk=comment_uuid)
    
    try:
        vt = VotedComments.objects.get(voted=cm.uuid)
    except VotedComments.DoesNotExist:
        cm.votes = cm.votes + 1
        cm.save()

        vt = VotedComments.objects.create(username=request.user.get_username(), voted=cm.uuid)
        vt.save()

    return redirect(request.META.get('HTTP_REFERER'))

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
            tp.save()

            return HttpResponseRedirect('/forum/')
    else:
        topic = NewTopic()

    return render(request, 'forum/newtopic.html', {'topic': topic})

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