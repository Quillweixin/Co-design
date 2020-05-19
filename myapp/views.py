from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from myapp.forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers
import json
from datetime import datetime,date
from myapp.models import Profile

# Create your views here.

def login_action(request):
    context = {}
    if request.method == 'GET':
        logout(request)
        context['form'] = LoginForm()
        return render(request,'login.html',context)
    form = LoginForm(request.POST)
    context['form'] = form
    # validate the form
    if not form.is_valid():
        return render(request, 'login.html', context)
    new_user = authenticate(request,username=form.cleaned_data['username'],
        password=form.cleaned_data['password'])
    login(request,new_user)
    return redirect(reverse('home'))

def home(request):
    return render(request,'home.html')

# get the user_info from the oauth provider
def oauth_login(request):
    user = request.user
    if not hasattr(user,"profile"):
        new_profile = Profile(owner=user,credibility=0,provider="google")
        new_profile.save()
    return redirect(reverse('home'))

def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request,'register.html',context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request,'register.html',context)
    # create new user
    new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                        password = form.cleaned_data['password'],
                                        email = form.cleaned_data['email'],
                                        first_name = form.cleaned_data['first_name'],
                                        last_name = form.cleaned_data['last_name'])
    new_user.save()
    new_profile = Profile(owner=new_user,credibility=0)
    new_profile.save()
    new_user = authenticate(request,username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('home'))

def about(request):
    return render(request,'about.html')

@login_required
def profile(request, profile_id):
    context = {}
    # profile id
    context['profile_id'] = profile_id
    # get the profile
    profile = Profile.objects.filter(id=profile_id)[0]
    context['profile'] = profile
    # get the task requests
    requests = profile.requests.all()
    context['requests'] = requests
    # get all tasks
    tasks = profile.tasks.all()
    context['tasks'] = tasks
    # form to upload avatar
    context['profile_form'] = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if not form.is_valid():
            context['profile'] = form
            return render(request,'profile.html',context)
        form.save()
        context['profile'] = profile

    return render(request,'profile.html',context)

def tasks(request):
    context = {}
    tasks = Task.objects.all().order_by('date')
    context['tasks'] = tasks
    return render(request,'tasks.html',context)

def details(request,id):
    context = {}
    task = Task.objects.filter(id=id)[0]
    context['task'] = task
    return render(request,'details.html',context)

@login_required
def post_request(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RequestForm()
        return render(request,'post_request.html',context)
    # received a request
    task = Task()
    form = RequestForm(request.POST,request.FILES,instance=task)
    if not form.is_valid():
        print(form.errors)
        context['form'] = form
        return render(request,'post_request.html',context)
    else:
        task.requester = request.user.profile
        form.save()
    return redirect(reverse('home'))

@login_required
def get_avatar(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.avatar:
        raise Http404
    return  HttpResponse(profile.avatar)

def task_image(request, id):
    task = get_object_or_404(Task, id=id)
    if not task.image:
        raise Http404
    return HttpResponse(task.image)

def work_image(request, id):
    work = get_object_or_404(Work, id=id)
    if not work.image:
        raise Http404
    return HttpResponse(work.image)


@login_required
def accept_task(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        profile = request.user.profile
        task = Task.objects.filter(id=task_id)[0]
        new_work = Work(author=profile,task=task)
        new_work.save()
        if not profile in task.workers.all():
            task.workers.add(profile)
            task.works.add(new_work)
    return details(request,task_id)

@login_required
def work(request):
    context = {}
    user = request.user
    task_id = request.GET['task_id']
    task = Task.objects.filter(id = task_id)[0]
    context['task'] = task
    work = user.profile.works.filter(task=task)[0]
    context['work'] = work

    # get all works on this task
    context['all_works'] = task.works.all()

    if request.method == 'POST':
        form = WorkForm(request.POST,request.FILES,instance=work)
        if not form.is_valid():
            print(form.errors)
            context['profile'] = form
            return render(request,'work.html',context)
        else:
            form.save()

    context['form'] = WorkForm(initial={'description':work.description})
    return render(request,'work.html',context)

@login_required
def review(request,id):
    context = {}
    task = Task.objects.filter(id=id)[0]
    context['task'] = task
    context['works'] = task.works.all()
    return render(request,'review.html',context)