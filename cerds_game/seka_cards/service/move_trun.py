from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json
import random



async def move_trun (self, room_id, nymber_player):
    nymber_player = int(nymber_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    player = next((player for player in players if player.trun == 3), None)
    number = player.number + 2 if player.number < nymber_player else player.number + 2 - nymber_player

    if player is None:
        player = next((player for player in players if player.trun == 4), None)
        number = player.number + 1 if player.number < nymber_player else player.number + 1 - nymber_player
    
    for p in players:
        if p.number == number:
            p.trun = 4
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



    