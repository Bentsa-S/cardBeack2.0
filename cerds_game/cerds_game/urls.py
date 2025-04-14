from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('durack/', include('durack_cards.urls')),
    path('seka/', include('seka_cards.urls')),
    path('players/', include('players.urls')),    
]
