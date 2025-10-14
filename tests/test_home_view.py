import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from estimation_app.models import Room, Player

@pytest.mark.django_db
def test_home_view_creates_room_and_player(client):
    """
    Test that submitting the HomeView form:
    - Creates a Room
    - Creates a temporary User
    - Creates a Player linked to that Room
    - Redirects to the room URL
    """
    # Arrange: form data
    data = {
        "name": "Alice",
    }

    # Act: post to the home view
    response = client.post(reverse("home"), data)

    # Assert: response is a redirect (302)
    assert response.status_code == 302

    # Check that a room was created
    assert Room.objects.count() == 1
    room = Room.objects.first()

    # Check that a user was created
    assert User.objects.count() == 1
    user = User.objects.first()
    assert "Alice" in user.username  # name is included in generated username

    # Check that a player was created and linked to the room
    assert Player.objects.count() == 1
    player = Player.objects.first()
    assert player.room == room
    assert player.user == user

    # Check redirect URL includes the room code
    assert str(room.code) in response.url
