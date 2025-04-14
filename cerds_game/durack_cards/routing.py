from django.urls import re_path
from .consumer import RyoomCardsGame

durack_router = [
    re_path(r'durack/(?P<number_players>\d+)/(?P<room_id>\d+)/$', RyoomCardsGame.as_asgi())
]
