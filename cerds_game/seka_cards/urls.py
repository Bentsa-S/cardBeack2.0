from django.urls import path
from . import views

urlpatterns = [
    path('create_room/', views.create_room_seka, name='create_item'),
    path('list_rooms/', views.list_rooms, name='create_item'),
]
