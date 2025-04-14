from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json


async def remove_player_room(self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    updated_order = []
    disconnect_user = None

    for i, player in enumerate(player_order):
        if player['name_room'] == self.channel_name:
            disconnect_user = player
            updated_order.append({
                "user": False,
                "number": i + 1
            })
        else:
            updated_order.append(player)

    if disconnect_user:
        print(disconnect_user['id'])
        print(disconnect_user)
        print(11111111)

    await database_sync_to_async(Room.objects.filter(id=room_id).update)(player_order=updated_order)

    message = {
        "type": "disconnect",
        "id": disconnect_user['id'] if disconnect_user else None
    }

    for player in players:
        await self.channel_layer.send(
            player.name_room,
            {
                'type': 'message',
                'message': message
            }
        )
