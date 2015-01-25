from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from twittclo_app.forms import AuthenticateForm, UserCreateForm, TwittcloForm
from twittclo_app.models import Twittclo

def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        twittclo_form = TwittcloForm()
        user = request.user
        twittclos_self = Twittclo.objects.filter(user=user.id)
        twittclos_buddies = Twittclo.objects.filter(user__userprofile__in=user.profile.follows.all)
        twittclos = twittclos_self | twittclos_buddies
 
        return render(request,
                      'buddies.html',
                      {'twittclo_form': twittclo_form, 'user': user,
                       'twittclos': twittclos,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')
 
 
def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')

from django.contrib.auth.decorators import login_required
 
@login_required
def submit(request):
    if request.method == "POST":
        twittclo_form = TwittcloForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if twittclo_form.is_valid():
            twittclo = twittclo_form.save(commit=False)
            twittclo.user = request.user
            twittclo.save()
            return redirect(next_url)
        else:
            return public(request, twittclo_form)
    return redirect('/')

@login_required
def public(request, twittclo_form=None):
    twittclo_form = twittclo_form or TwittcloForm()
    twittclos = Twittclo.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'twittclo_form': twittclo_form, 'next_url': '/twittclos',
                   'twittclos': twittclos, 'username': request.user.username})

from django.db.models import Count
from django.http import Http404
 
 
def get_latest(user):
    try:
        return user.twittclo_set.order_by('-id')[0]
    except IndexError:
        return ""
 
 
@login_required
def users(request, username="", twittclo_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        twittclos = Twittclo.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'twittclos': twittclos, })
        return render(request, 'user.html', {'user': user, 'twittclos': twittclos, 'follow': True, })
    users = User.objects.all().annotate(twittclo_count=Count('twittclo'))
    twittclos = map(get_latest, users)
    obj = zip(users, twittclos)
    twittclo_form = twittclo_form or TwittcloForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'twittclo_form': twittclo_form,
                   'username': request.user.username, })

from django.core.exceptions import ObjectDoesNotExist
 
@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')