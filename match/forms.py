from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import MatchPost


#class MyUserCreationForm(UserCreationForm):
    # class Meta:
        # model = User

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'title', 'style': 'width: 300px;'}))
    game_type = forms.ChoiceField(choices=MatchPost.GameType.choices)
    game_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'style': 'width: 300px;'}))
    content = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'title', 'style': 'width: 300px;'}))
    game_spot = forms.CharField(max_length=100)
    class Meta:
        model = MatchPost
        fields = ['title', 'game_date',"game_type", "content"]
    # def __init__(self, *args, **kwargs):
    #     game_spot_name = kwargs.pop('game_spot', '')
    #     print(kwargs, 'abc')
    #     GameSpot.objects.get_or_create(name=game_spot_name)
    #     super().__init__(*args, **kwargs)
    #     self.fields['game_spot'] = forms.ModelChoiceField(queryset=GameSpot.objects.filter(name=game_spot_name))

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']