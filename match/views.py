import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MatchPost, GameSpot
from .forms import PostForm, MyUserCreationForm
from django.views import generic
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'match/index.html'
    context_object_name = "post_list"
    def get_queryset(self):
        return MatchPost.objects.filter(game_date__gte=datetime.date.today()).order_by('game_date')

class DetailView(generic.DetailView):
    model = MatchPost
    template_name = 'match/detail.html'
    context_object_name = "post"

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect(reverse('match:index'))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect(reverse('match:index'))
        else:
            messages.error(request, 'Email or password is incorrect')
    context = {'page': page}
    return render(request, 'match/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('match:login')

def register(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            django_login(request, user)
            return redirect(reverse('match:index'))
        else:
            messages.error(request, 'An error has occurred during registration')
    return render(request,'match/login_register.html', {'page': "register", 'form': form})

@login_required(login_url='match:login')
def write(request):
    places = GameSpot.objects.values_list("name", flat=True)
    game_types = (x[0] for x in MatchPost.GameType.choices)
    return render(request, 'match/post_form.html', {'places': places, 'game_types':game_types})

def confirm(request):
    game_spot = request.POST.get('game_spot', '')
    form = PostForm(request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.game_spot = GameSpot.objects.get(name=game_spot)
        new_post.save()
        form.save_m2m()
        return render(request, 'match/confirm.html', {'form': form})
    return redirect(reverse('match:write'))
