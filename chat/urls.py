from django.urls import path
from chat.views import chatroom

app_name = "chat"
urlpatterns = [
    path("<uuid:uuid>/", chatroom.room, name="room"),
]