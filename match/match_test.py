import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from .models import MatchPost


@pytest.fixture
def api_client():
    user = User.objects.create(username='jenny', password='password')
    client = Client()
    client.force_login(user=user)
    return client

@pytest.mark.django_db
def test_write_confirm_view_success_with_200(api_client):
    MatchPost.objects.create(name='88테니스')
    data = {'title': '사람구해요', 'game_date': '2023-12-25', 'game_spot': '88테니스', 'game_type': 'single', 'content': '사람 구해요 고수만. 한수요',}
    response = api_client.post(reverse('match:confirm'), data=data)
    assert response.status_code == 200

    response = api_client.get(reverse('match:index'))
    assert response.status_code == 200
    instance = response.context['post_list'].first()
    assert instance.title == '사람구해요'
    assert instance.game_spot.name == '88테니스'
