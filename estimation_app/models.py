# models.py
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.code}"


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="players")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.room.code}"


class Vote(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="vote")
    value = models.CharField(max_length=5)  # "1", "2", "3", "5", "8", "13", "?"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.user.username} -> {self.value}"
