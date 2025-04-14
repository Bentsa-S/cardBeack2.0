from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json
import random
from .calculate_seka_score import calculate_seka_score 


async def look_card_trun (self, room_id, number_player, idPlayer):
    number_player = int(number_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order        
    player_cards_order = room.player_cards_order
    id_player_to_loos = 0
    player = next((player for player in player_order if idPlayer == player['id']), None)


    for index in range(1, number_player):
        player_trun_number = (player['number'] - index) % number_player or number_player
        playerTrun = next((p for p in player_order if player_trun_number == p['number']), None)

        if playerTrun['pass']:
            player_trun_number = (player['number'] - index - 1) % number_player or number_player
            playerTrun = next((p for p in player_order if player_trun_number == p['number']), None)
        else:
            break
    
    player_cards_open = next((player for player in player_cards_order if idPlayer == player['id']), None)
    if number_player == 2:
        player_cards_trun = next((player for player in player_cards_order if player['id'] != idPlayer), None)
    else:
        player_cards_trun = next((player for player in player_cards_order if player_trun_number == player['number']), None)

    player_points_open = calculate_seka_score(player_cards_open['cards'])
    player_points_trun = calculate_seka_score(player_cards_trun['cards'])


    if player_points_open > player_points_trun or player_points_open == player_points_trun:
        playerTrun = next((p for p in player_order if player_cards_trun['id'] == p['id']), None)
        playerTrun['pass'] = True
        id_player_to_loos = playerTrun['id']
        sensor_to_win = True
    else:
        playerTrun = next((p for p in player_order if player_cards_open['id'] == p['id']), None)
        playerTrun['pass'] = True
        id_player_to_loos = playerTrun['id']
        sensor_to_win = False




    pass_count = sum(1 for p in player_order if p['pass'])
    print(pass_count)
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
            
    
    win_player_open = {
        'type': 'look',
        'loos': sensor_to_win,
        'id_loos': player_cards_open['id'],
        'id_win': player_cards_trun['id'],
        'cards': player_cards_trun['cards']  # Карти опонента
    }

    win_player_trun = {
        'type': 'look',
        'loos': not sensor_to_win,
        'id_loos': player_cards_trun['id'],
        'id_win': player_cards_open['id'],
        'cards': player_cards_open['cards']  # Карти опонента
    }

    await self.channel_layer.send(
        player_cards_open['name_room'],
        {
            'type': 'message',
            'message': win_player_open
        }
    )

    await self.channel_layer.send(
        player_cards_trun['name_room'],
        {
            'type': 'message',
            'message': win_player_trun
        }
    )

    pass_player = {
        'type': 'pass',
        'id': id_player_to_loos
    }
    for player in player_order:
        if player['name_room'] not in [player_cards_open['name_room'], player_cards_trun['name_room']]:
            await self.channel_layer.send(
                player['name_room'],
                {
                    'type': 'message',
                    'message': pass_player
                }
            )


