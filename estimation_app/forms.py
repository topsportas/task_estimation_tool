from django import forms

class CreateRoomForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your Name")

class JoinRoomForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your Name")
    code = forms.CharField(max_length=10, label="Room Code")