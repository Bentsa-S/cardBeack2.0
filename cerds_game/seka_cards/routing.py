from django.urls import re_path
from .consumer import RyoomCardsSeka

seka_router = [
    re_path(r'seka/(?P<number_players>\d+)/(?P<room_id>\d+)/(?P<bet>\d+)/$', RyoomCardsSeka.as_asgi()),
]
