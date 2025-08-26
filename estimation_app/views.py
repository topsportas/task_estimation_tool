from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import random

from .models import Room, Player, Vote

SCRUM_POKER_CARDS = ["0", "0.5", "1", "2", "3", "5", "8", "13", "20", "40", "100", "?"]


class HomeView(TemplateView):
    template_name = "estimation_app/home.html"
    def post(self, request, *args, **kwargs):
        # Generate random 6-digit code
        code = str(random.randint(100000, 999999))
        from .models import Room
        Room.objects.create(code=code)
        return redirect('room', code=code)

class RoomView(TemplateView):
    template_name = "estimation_app/poker_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = get_object_or_404(Room, code=self.kwargs["code"])
        context["room"] = room
        context["cards"] = SCRUM_POKER_CARDS
        return context

class SubmitVoteView(View):
    def post(self, request, code):
        try:
            data = json.loads(request.body)
            card_value = data.get("value")
            room = get_object_or_404(Room, code=code)

            # Use session key instead of user
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            player, _ = Player.objects.get_or_create(user=None, room=room)

            vote, _ = Vote.objects.update_or_create(
                player=player,
                defaults={"value": card_value}
            )
            # return JsonResponse({"success": True, "vote": vote.value})
            return JsonResponse({"success": True, "vote": vote.value})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

