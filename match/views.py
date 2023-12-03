import datetime

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import MessageForm, MyUserCreationForm, PostForm, UserForm
from .models import Conversation, GameSpot, MatchPost, Message, User


class IndexView(generic.ListView):
    template_name = 'match/index.html'
    context_object_name = "post_list"

    def get_queryset(self):
        return MatchPost.objects.filter(
            game_date__gte=datetime.date.today()).order_by('game_date')


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
            messages.error(request,
                           'An error has occurred during registration')
    return render(request, 'match/login_register.html', {
        'page': "register",
        'form': form
    })


@login_required(login_url='match:login')
def write(request):
    places = GameSpot.objects.values_list("name", flat=True)
    game_types = (x[0] for x in MatchPost.GameType.choices)
    return render(request, 'match/post_form.html', {
        'places': places,
        'game_types': game_types
    })


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


@login_required(login_url='match:login')
def conversation(request, post, host, guest):
    con, _ = Conversation.objects.get_or_create(match_post_id=post,
                                                host_id=host,
                                                guest_id=guest)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.sender = request.user
            new_msg.conversation = con
            new_msg.save()
            form.save_m2m()
    messages = con.message_set.all()
    return render(
        request, 'match/conversation.html', {
            'messages': messages,
            'user': request.user,
            'post': post,
            'host': host,
            'guest': guest
        })


@login_required(login_url='match:login')
def conversation_list(request):
    user = request.user
    counter = User.objects.filter(id=OuterRef("guest_id")).values('username')
    last_message = Message.objects.filter(conversation_id=OuterRef(
        'id')).values('content').order_by('-created_at')[:1]
    last_datetime = Message.objects.filter(conversation_id=OuterRef(
        'id')).values('created_at').order_by('-created_at')[:1]
    hosted_con = Conversation.objects.filter(host_id=user.id).annotate(
        counter=counter,
        last_message=last_message,
        last_datetime=last_datetime)
    guest_con = Conversation.objects.filter(guest_id=user.id).annotate(
        counter=counter,
        last_message=last_message,
        last_datetime=last_datetime)
    return render(request, 'match/conversation_list.html', {
        'hosted_con': hosted_con,
        'guest_con': guest_con
    })


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    posts = MatchPost.objects.filter(user=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'match/profile.html', context)


def update_user(request):
    user = request.user
    form = UserForm(user)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('match:profile', args=(user.id, )))
    return render(request, 'match/update_profile.html')
