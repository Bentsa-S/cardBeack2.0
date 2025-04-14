import os

# Встановлюємо змінну оточення перед викликом get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerds_game.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from durack_cards.routing import durack_router 
from seka_cards.routing import seka_router

websocket_urlpatterns = durack_router + seka_router

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
