from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room

@api_view(['POST'])
def create_room_seka(request):
    if request.method == 'POST':
        # Отримуємо дані з запиту
        participants = request.data.get("participants", 2)
        seven = request.data.get("seven", False)
        rate = request.data.get("rate", 0.0)
        bet = request.data.get("sliderBet", 0)
        isPrivate = request.data.get("isPrivate", False)
        password = request.data.get("password", 0)
        hew = request.data.get("attack", False)
        push = request.data.get("draw", False)
        cards = request.data.get("cards", [])
        player_order = request.data.get("player_order", [])

        # Створюємо нову кімнату
        room = Room.objects.create(
            participants=participants,
            # seven=seven,
            rate=rate,
            isPrivate=isPrivate,
            password=password,
            hew=hew,
            bet=bet,
            push=push,
            cards=cards,
            player_order=player_order
        )

        message = {
            "room_id": room.id,
            "create": True,
            "bet": bet
        }
        return Response(message, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_rooms(request):
    rooms = Room.objects.all()
    if not rooms:
        return Response({"message": "Немає доступних кімнат."}, status=status.HTTP_404_NOT_FOUND)
    
    room_data = []
    for room in rooms:
        room_data.append({
            "game": "seka",
            "room_id": room.id,
            "participants": room.participants,
            "rate": room.rate,
            "bet": room.bet
        })
    # Room.objects.all().delete()

    return Response(room_data, status=status.HTTP_200_OK)
