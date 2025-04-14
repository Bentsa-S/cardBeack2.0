from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.create_user, name='create_user'),
    path('get-user/', views.get_user, name='get_user'),
    path('get-friends/', views.get_friends_view, name='get_friends'),
    path('add-friend/', views.add_friend_view, name='add_friend'),
    path('remove-friend/', views.remove_friend_view, name='remove_friend'),
    path('send-message/', views.send_telegram_message),

]
