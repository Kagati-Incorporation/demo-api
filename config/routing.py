import notifications.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from notifications.token_authentication_stack import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})
