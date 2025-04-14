from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json
import random



async def redy_take_trun (self, room_id, number_player):
    number_player = int(number_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order


    player_order_trun = next((player for player in players if player.trun == 1), None)
    player = next((player for player in player_order if player_order_trun.name_room == player['name_room']), None)

    number = (player['number'] - 1) % number_player or number_player

    playerTrun = next((p for p in player_order if number == p['number']), None)

    
    for p in players:
        if p.name_room == playerTrun['name_room']:
            p.trun = 3
        else:
            p.trun = 4
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



    