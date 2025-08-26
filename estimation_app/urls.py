# urls.py
from django.urls import path
from .views import RoomView, SubmitVoteView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("room/<str:code>/", RoomView.as_view(), name="room"),
    path("room/<str:code>/vote/", SubmitVoteView.as_view(), name="submit_vote"),
]
