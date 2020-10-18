from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from scrap.models import Scrap
from .models import Contact, Profile
from django.core.paginator import Paginator
from . models import News



@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    scrap = request.POST.get('parent')
    #print(scrap)
    #print(user_id)
    #print(action)
    tp = Scrap.objects.filter(id=scrap)
    if user_id and action:
        try:
            user = Profile.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user=user,
                                              topic=tp[0])
            else:
                Contact.objects.filter(user=user,
                                              topic=tp[0]).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'ok'})




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'users/user/list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    posts = Scrap.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'users/user/detail.html', {'section':'people', 'user': user, 'page_obj': page_obj})


@login_required
def feed(request):
    t_ids = {
        3 : "Movies",
        1 : "sports",
        2 : "Games",
        4 : "HackerNews RSS"
    }
    user = get_object_or_404(User, username=request.user, is_active=True)
    user_id = user.id
    source_id = list(Contact.objects.filter(user_id=user_id).values('topic_id'))
    #source = t_ids.get(source_id[0].get('topic_id'))
    #print(source)
    
    scraps = News.objects.none()
    
    for i in range(len(source_id)):
        print(t_ids.get(source_id[i].get('topic_id')))
        scraps_temp = News.objects.filter(source=t_ids.get(source_id[i].get('topic_id')))
        scraps = (scraps | scraps_temp)
        print(scraps)
        print(scraps_temp)


    #scraps = News.objects.filter(source=source).order_by('-id')



    paginator = Paginator(scraps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/feed.html', {'scraps': scraps, 'user': user, 'page_obj': page_obj})