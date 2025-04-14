from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json
import random



async def pass_trun (self, room_id, number_player, idPlayer):
    number_player = int(number_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order        

    player_order_trun = next((player for player in players if player.trun == 5), None)
    player = next((player for player in player_order if player_order_trun.name_room == player['name_room']), None)
    player['pass'] = True

    await database_sync_to_async(Room.objects.filter(id=room_id).update)(player_order=player_order)


    for index in range(1, number_player):
        player_trun_number = (player['number'] + index) % number_player or number_player
        playerTrun = next((p for p in player_order if player_trun_number == p['number']), None)

        if playerTrun['pass']:
            player_trun_number = (player['number'] + index + 1) % number_player or number_player
            playerTrun = next((p for p in player_order if player_trun_number == p['number']), None)
        else:
            break
    

    pass_count = sum(1 for p in player_order if p['pass'])

    if pass_count == number_player - 1:
        for player in player_order:
            if not player['pass']:
                player_win = player
            
        win_player = {
            'type': 'win',
            'id': player_win['id']
        }
        for p in players:
            await self.channel_layer.send(
                p.name_room,
                {
                    'type': 'message',
                    'message': win_player
                }
            )





    for p in players:
        p.trun = 5 if p.name_room == playerTrun['name_room'] and pass_count != number_player - 1 else 6

        if playerTrun["GameRound"] > 0:
            hideOpponentButton = {
                'type': 'hideOpponentButton',
            } 

            await self.channel_layer.send(
                p.name_room,
                {
                    'type': 'message',
                    'message': hideOpponentButton
                }
            )

        await database_sync_to_async(p.save)()
        
        player_message = {
            'type': 'playerStatus',
            'playerStatus': p.trun,
        } 

        pass_player = {
            'type': 'pass',
            'id': idPlayer
        }

        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': pass_player
            }
        )

        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': player_message
            }
        )
