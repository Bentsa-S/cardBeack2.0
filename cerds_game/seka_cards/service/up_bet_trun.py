from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json
import random



async def up_bet_trun (self, room_id, number_player, bet):
    number_player = int(number_player)
    bet = int(bet)
        
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order   

    player_order_trun = next((player for player in players if player.trun == 5), None)
    player = next((player for player in player_order if player_order_trun.name_room == player['name_room']), None)

    player["GameRound"] += 1

    playerDatabase = await database_sync_to_async(Player.objects.get)(id=player_order_trun.player_id)
    playerDatabase.prise -= bet
    room.bank += bet

    if room.bleackMove:
        if player['bleack']:
            bet = bet * 2

    room.bet = bet

    await database_sync_to_async(room.save)()
    await database_sync_to_async(playerDatabase.save)()
    number = (player['number'] + 1) % number_player or number_player

    playerTrun = next((p for p in player_order if number == p['number']), None)

    if room.bleackMove:
        if playerTrun['bleack']:
            bet = bet / 2
            
    prise = {
        'type': 'prise',
        'prise': playerDatabase.prise
    }
    await self.send(text_data=json.dumps(
        {
            'type': 'message',
            'message': prise
        }
    ))

    for p in players:
        if p.name_room == playerTrun['name_room']:
            p.trun = 5
        else:
            p.trun = 6

        await database_sync_to_async(p.save)()

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
        
        player_message = {
            'type': 'playerStatus',
            'playerStatus': p.trun,
        } 

        apdateTable = {
            'type': 'apdateTable',
            'bet': bet,
            'bank': room.bank
        } 

        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': apdateTable
            }
        )

        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': player_message
            }
        )
