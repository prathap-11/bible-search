# your_project_name/asgi.py

# import os
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# application = get_asgi_application()

# your_project_name/asgi.py

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from myapp.routing import websocket_urlpatterns  # Import your routing file from the app

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # This handles regular HTTP requests
#     "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
#         URLRouter(
#             websocket_urlpatterns  # This is where your WebSocket URL patterns are defined
#         )
#     ),
# })

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from myapp.routing import websocket_urlpatterns  # Ensure this import is correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # This handles regular HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
        URLRouter(
            websocket_urlpatterns  # This is where your WebSocket URL patterns are defined
        )
    ),
})

