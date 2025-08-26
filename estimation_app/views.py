import json
import random
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from .models import Room, Player, Vote
from django.utils.crypto import get_random_string

SCRUM_POKER_CARDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

class CreateRoomForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your Name")

class JoinRoomForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your Name")
    code = forms.CharField(max_length=10, label="Room Code")

class JoinRoomView(View):
    template_name = "estimation_app/join_room.html"

    def get(self, request, *args, **kwargs):
        form = JoinRoomForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            code = form.cleaned_data["code"]

            # Check if room exists
            try:
                room = Room.objects.get(code=code)
            except Room.DoesNotExist:
                return render(request, self.template_name, {
                    "form": form,
                    "error": "Room not found."
                })

            # Create temporary user
            username = f"{name}_{get_random_string(4)}"
            user = User.objects.create(username=username)

            # Save username in session
            request.session["player_username"] = user.username
            request.session.save()

            # Add player to room
            Player.objects.create(user=user, room=room)

            return redirect("room", code=room.code)

        return render(request, self.template_name, {"form": form})

class HomeView(TemplateView):
    template_name = "estimation_app/home.html"

    def get(self, request, *args, **kwargs):
        form = CreateRoomForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            # Generate random 6-digit code
            code = str(random.randint(100000, 999999))
            room = Room.objects.create(code=code)

            # Create temporary user
            username = f"{name}_{get_random_string(4)}"
            user = User.objects.create(username=username)

            # Save username in session
            request.session["player_username"] = user.username
            request.session.save()

            # Add player to room
            Player.objects.create(user=user, room=room)

            # Redirect to the room
            return redirect("room", code=room.code)
        return render(request, self.template_name, {"form": form})

class RoomView(TemplateView):
    template_name = "estimation_app/poker_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = get_object_or_404(Room, code=self.kwargs["code"])
        context["room"] = room
        context["cards"] = SCRUM_POKER_CARDS
        # Get current player from session
        username = self.request.session.get("player_username")
        player = None
        if username:
            player = room.players.filter(user__username=username).first()
        context["current_player"] = player

        # List all players
        context["players"] = room.players.select_related("user").all()
        return context

class SubmitVoteView(View):
    def post(self, request, code):
        try:
            data = json.loads(request.body)
            card_value = data.get("value")
            room = get_object_or_404(Room, code=code)


            # Get current player from session
            username = request.session.get("player_username")
            if not username:
                return JsonResponse({"success": False, "error": "Player not found in session"}, status=400)

            player = get_object_or_404(Player, user__username=username, room=room)

            # Save or update vote
            vote, _ = Vote.objects.update_or_create(
                player=player,
                defaults={"value": card_value}
            )
            return JsonResponse({"success": True, "vote": vote.value})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

class RoomStateView(View):
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
