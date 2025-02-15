# routing.py
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/verse/$', consumers.VerseConsumer.as_asgi()),
# ]

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/verse/$', consumers.VerseConsumer.as_asgi()),
]
