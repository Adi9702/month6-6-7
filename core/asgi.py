# тут мы обычный http запрос заменили на вебсокет
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from app.chat.middleware import QueryParamJWTAuthMiddleware
from app.chat.routing import websocket_urlpatterns as chat_ws
from app.notification.routing import websocket_urlpatterns as notif_ws

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": QueryParamJWTAuthMiddleware(
            URLRouter(chat_ws)
        ),
    }
)