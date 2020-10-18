from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Scrap
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Value, IntegerField
from scraping.models import News
from users.models import Contact






def scrap_list_view(request):
    scraps = News.objects.all().order_by('-id')
    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cts = []
    contacts = Contact.objects.filter(user_id=request.user.id).values()
    for i in range(len(contacts)):
        print(contacts[i].get('topic_id'))
        cts.append(contacts[i].get('topic_id'))
        print(cts)

    return render(request, 'scrap/home.html', {'scraps': scraps, 'cts': cts,'page_obj': page_obj})

def movie_list_view(request):
    scraps = News.objects.filter(source="Movies").order_by('-id')
    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cts = []

    contacts = Contact.objects.filter(user_id=request.user.id).values()
    for i in range(len(contacts)):
        print(contacts[i].get('topic_id'))
        cts.append(contacts[i].get('topic_id'))
        print(cts)

    return render(request, 'scrap/movies.html', {'scraps': scraps,'cts': cts, 'page_obj': page_obj})

def sports_list_view(request):
    scraps = News.objects.filter(source="sports").order_by('-published')
    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cts = []
    contacts = Contact.objects.filter(user_id=request.user.id).values()
    for i in range(len(contacts)):
        print(contacts[i].get('topic_id'))
        cts.append(contacts[i].get('topic_id'))
        print(cts)

    return render(request, 'scrap/sports.html', {'scraps': scraps,'cts': cts, 'page_obj': page_obj})

def hacks_list_view(request):
    scraps = News.objects.filter(source="HackerNews RSS").order_by('-id')
    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cts = []
    contacts = Contact.objects.filter(user_id=request.user.id).values()
    for i in range(len(contacts)):
        print(contacts[i].get('topic_id'))
        cts.append(contacts[i].get('topic_id'))
        print(cts)

    return render(request, 'scrap/hacks.html', {'scraps':scraps, 'cts': cts, 'page_obj': page_obj})

def games_list_view(request):
    scraps = News.objects.filter(source="Games").order_by('-id')
    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cts = []
    contacts = Contact.objects.filter(user_id=request.user.id).values()
    for i in range(len(contacts)):
        print(contacts[i].get('topic_id'))
        cts.append(contacts[i].get('topic_id'))
        print(cts)

    return render(request, 'scrap/games.html', {'scraps':scraps, 'cts': cts, 'page_obj': page_obj})



def about(request):
    return render(request, 'scrap/about.html', {'title': 'about'})

