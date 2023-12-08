from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import GameSpot, MatchPost, Message, User


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'title',
                                'style': 'width: 300px;'
                            }))
    game_type = forms.ChoiceField(choices=MatchPost.GameType.choices)
    game_date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={'style': 'width: 300px;'}))
    content = forms.TextInput()
    game_spot = MyModelChoiceField(queryset=GameSpot.objects.all(),
                                   to_field_name="name")

    class Meta:
        model = MatchPost
        fields = ['title', 'game_date', "game_type", "content"]

    # def __init__(self, *args, **kwargs):
    #     game_spot_name = kwargs.pop('game_spot', '')
    #     print(kwargs, 'abc')
    #     GameSpot.objects.get_or_create(name=game_spot_name)
    #     super().__init__(*args, **kwargs)
    #     self.fields['game_spot'] = forms.ModelChoiceField(queryset=GameSpot.objects.filter(name=game_spot_name))


class MessageForm(forms.ModelForm):
    content = forms.TextInput()

    class Meta:
        model = Message
        fields = ['content']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'bio']
