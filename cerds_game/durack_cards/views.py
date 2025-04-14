from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room

@api_view(['POST'])
def create_room(request):
    if request.method == 'POST':
        # Отримуємо дані з запиту
        participants = request.data.get("participants", 2)
        deck = request.data.get("deck", 36)
        rate = request.data.get("rate", 0.0)
        isPrivate = request.data.get("isPrivate", False)
        password = request.data.get("password", 0)
        attack = request.data.get("attack", False)
        draw = request.data.get("draw", False)
        cheater = request.data.get("cheater", False)
        transfer = request.data.get("transfer", False)
        cards = request.data.get("cards", [])
        player_order = request.data.get("player_order", [])

        # Створюємо нову кімнату
        room = Room.objects.create(
            participants=participants,
            deck=deck,
            rate=rate,
            isPrivate=isPrivate,
            password=password,
            attack=attack,
            draw=draw,
            cheater=cheater,
            transfer=transfer,
            cards=cards,
            player_order=player_order
        )

        message = {
            "room_id": room.id,
            "create": True,
        }
        return Response(message, status=status.HTTP_201_CREATED)