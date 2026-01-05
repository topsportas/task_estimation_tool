import json
import uuid
from django.views.generic import TemplateView, View, FormView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Room, Player, Vote
from .forms import CreateRoomForm, JoinRoomForm
from .constants import SCRUM_POKER_CARDS


class JoinRoomView(LoginRequiredMixin, FormView):
    template_name = "roomapp/join_room.html"
    form_class = JoinRoomForm

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        # Check if room exists
        room = get_object_or_404(Room, code=code)
        user = self.request.user
        # Check if the player already exists in this room
        player, created = Player.objects.get_or_create(user=user, room=room)
        return redirect("room", code=room.code)


class HomeView(LoginRequiredMixin, FormView):
    template_name = "roomapp/home.html"
    form_class = CreateRoomForm

    def form_valid(self, form):
        code = uuid.uuid4().hex[:8]
        room = Room.objects.create(code=code)
        user = self.request.user
        # Add player to room
        Player.objects.create(user=user, room=room)

        # Redirect to the room
        return redirect("room", code=room.code)


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "roomapp/poker_room.html"

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
    def post(self, request, code):
        try:
            data = json.loads(request.body)
            card_value = data.get("value")
            room = get_object_or_404(Room, code=code)
            player = get_object_or_404(Player, user__username=request.user, room=room)

            # Save or update vote
            vote, _ = Vote.objects.update_or_create(
                player=player, defaults={"value": card_value}
            )
            return JsonResponse({"success": True, "vote": vote.value})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class RoomStateView(LoginRequiredMixin, View):
    def get(self, request, code):
        room = get_object_or_404(Room, code=code)
        players = room.players.select_related("user").all()
        data = []
        for player in players:
            vote = player.vote.value if hasattr(player, "vote") else None
            data.append({"name": player.user.username, "vote": vote})
        return JsonResponse({"players": data})
