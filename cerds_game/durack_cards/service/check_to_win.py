from channels.db import database_sync_to_async
from durack_cards.models import Room
import json



async def check_to_win(self, room_id, id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())

    for p in players:
        win_player = {
            'type': 'win',
            'id': id
        }
        for p in players:
            await self.channel_layer.send(
                p.name_room,
                {
                    'type': 'message',
                    'message': win_player
                }
            )
