from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json
import random



async def take_trun (self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    for p in players:
        if self.channel_name != p.name_room:
            massege = {
                'type': 'take'
            }
            await self.channel_layer.send(
                p.name_room,
                {
                    'type': 'message',
                    'message': massege,
                }
            )



    