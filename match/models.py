from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=50, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="sevage.jpeg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class MatchPost(models.Model):
    class GameType(models.TextChoices):
        single = 'single', "단식"
        mix_single = 'mix_single', "단식(성별 무관)"
        w_double = 'w_double', "여복"
        m_double = 'm_double', "남복"
        mix_double = "mix_double", "복식(성별 무관)"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    game_date = models.DateTimeField(help_text='게임 날짜')
    game_spot = models.ForeignKey(to='GameSpot',
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  help_text='게임 장소')
    game_type = models.CharField(max_length=100,
                                 choices=GameType.choices,
                                 help_text='게임 타입')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False)


class GameSpot(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)


class Conversation(models.Model):
    match_post = models.ForeignKey(MatchPost, on_delete=models.CASCADE)
    host_id = models.IntegerField()
    guest_id = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation,
                                     on_delete=models.CASCADE,
                                     null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)
