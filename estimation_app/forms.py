from django import forms
from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateRoomForm(forms.Form):
    pass

class JoinRoomForm(forms.Form):
    code = forms.CharField(max_length=10, label="Room Code")

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not Room.objects.filter(code=code).exists():
            raise forms.ValidationError("Room not found.")
        return code

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

