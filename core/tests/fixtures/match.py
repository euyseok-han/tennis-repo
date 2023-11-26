import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from match.models import GameSpot


@pytest.fixture
def create_game_spot():
    return baker.make(GameSpot, name='88테니스')


@pytest.fixture
def api_client():
    return APIClient()
