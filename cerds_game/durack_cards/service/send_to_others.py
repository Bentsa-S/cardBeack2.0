from channels.db import database_sync_to_async
from durack_cards.models import Room
import json



async def send_to_others(self, room_id, message):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())

    for p in players:
        if p.name_room != self.channel_name:
            await self.channel_layer.send(
                p.name_room,
                {
                    'type': 'message',
                    'message': message
                }
            )
