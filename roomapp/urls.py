from django.urls import path
from .views import HomeView, JoinRoomView, RoomView, SubmitVoteView, RoomStateView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("join/", JoinRoomView.as_view(), name="join_room"),
    path("<str:code>/", RoomView.as_view(), name="room"),
    path("<str:code>/vote/", SubmitVoteView.as_view(), name="submit_vote"),
    path("<str:code>/state/", RoomStateView.as_view(), name="room_state"),
]
