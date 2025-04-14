from channels.db import database_sync_to_async
from durack_cards.models import Room
from players.models import Player
import json


async def add_player_room(self, json, room_id, number):
    trun = 0
    number = int(number)

    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    playerDatabase = await database_sync_to_async(Player.objects.get)(user_id=json.get('id'))
    player = await room.add_player(playerDatabase.name, self.channel_name, trun, playerDatabase.user_id, redy=False)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    if not player_order:
        order = [None] * number
    else:
        order = player_order
    
    for i in range(len(order)):
        if order[i] is None or not order[i]["user"]:
            order[i] = {
                "user": True,
                "name": json.get('name'),
                "name_room": self.channel_name,
                "number": i + 1,
                "trun": 0,
                "id": json.get('id'),
                "pass": False,
                "prise": playerDatabase.prise
            }
            break  # Stop after filling the first None

    for i in range(number):
        if order[i] is None:
            order[i] = {
                "user": False,
                "number": i + 1
            }
    message = {
        "type": "name",
        "order": order
    }
    # Надсилання оновленого порядку всім гравцям
    for player in players:
        await self.channel_layer.send(
            player.name_room,
            {
                'type': 'message',
                'message': message
            }
        )

    # Оновлюємо `player_order` у базі
    await database_sync_to_async(Room.objects.filter(id=room_id).update)(player_order=order)
