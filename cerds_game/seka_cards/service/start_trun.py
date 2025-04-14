from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json
import random



async def start_trun (self, room_id, nymber_player):
    nymber_player = int(nymber_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    random_player = random.randint(1, nymber_player)

    player = next((player for player in player_order if player['number'] == random_player), None)

    
    for p in players:
        if p.name_room == player['name_room']:
            p.trun = 1
        else:
            p.trun = 2
        await database_sync_to_async(p.save)()
        
        player_message = {
            'type': 'playerStatus',
            'playerStatus': p.trun
        } 
        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': player_message
            }
        )



    