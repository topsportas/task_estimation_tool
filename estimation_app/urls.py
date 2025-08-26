# urls.py
from django.urls import path
from .views import RoomView, SubmitVoteView, HomeView, JoinRoomView, RoomStateView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("room/<str:code>/", RoomView.as_view(), name="room"),
    path("room/<str:code>/vote/", SubmitVoteView.as_view(), name="submit_vote"),
    path("join/", JoinRoomView.as_view(), name="join_room"),
    path("room/<str:code>/state/", RoomStateView.as_view(), name="room_state"),
]
