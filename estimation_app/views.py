import json
import random
from django.views.generic import TemplateView, View, FormView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Room, Player, Vote
from .forms import CreateRoomForm, JoinRoomForm
from django.contrib.auth.views import LoginView

SCRUM_POKER_CARDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


class JoinRoomView(LoginRequiredMixin, FormView):
    template_name = "estimation_app/join_room.html"
    form_class = JoinRoomForm
    login_url = "/login/"

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        # Check if room exists
        room = get_object_or_404(Room, code=code)
        user = self.request.user
        # Check if the player already exists in this room
        player, created = Player.objects.get_or_create(user=user, room=room)
        return redirect("room", code=room.code)


class HomeView(LoginRequiredMixin, FormView):
    template_name = "estimation_app/home.html"
    form_class = CreateRoomForm
    login_url = "/login/"

    def form_valid(self, form):
        # Generate random 6-digit code
        code = str(random.randint(100000, 999999))
        room = Room.objects.create(code=code)
        user = self.request.user
        # Add player to room
        Player.objects.create(user=user, room=room)

        # Redirect to the room
        return redirect("room", code=room.code)


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "estimation_app/poker_room.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = get_object_or_404(Room, code=self.kwargs["code"])
        context["room"] = room
        context["cards"] = SCRUM_POKER_CARDS
        # Get current player for logged-in user
        player = room.players.filter(user=self.request.user).first()
        context["current_player"] = player

        # List all players
        context["players"] = room.players.select_related("user").all()
        return context


class SubmitVoteView(LoginRequiredMixin, View):
    login_url = "/login/"
    def post(self, request, code):
        try:
            data = json.loads(request.body)
            card_value = data.get("value")
            room = get_object_or_404(Room, code=code)

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"success": False, "error": "User not authenticated"}, status=403)
            player = get_object_or_404(Player, user__username=user, room=room)

            # Save or update vote
            vote, _ = Vote.objects.update_or_create(
                player=player,
                defaults={"value": card_value}
            )
            return JsonResponse({"success": True, "vote": vote.value})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class RoomStateView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, code):
        room = get_object_or_404(Room, code=code)
        players = room.players.select_related("user").all()
        data = []
        for player in players:
            vote = player.vote.value if hasattr(player, "vote") else None
            data.append({
                "name": player.user.username,
                "vote": vote
            })
        return JsonResponse({"players": data})

class UserLoginView(LoginView):
    template_name = "estimation_app/login.html"