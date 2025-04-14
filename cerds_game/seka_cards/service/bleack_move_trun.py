from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json



async def bleack_move_trun (self, room_id, number_player):
    number_player = int(number_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order
    if not room.bleackMove:
        room.bleackMove = True

    player_order_trun = next((player for player in players if player.trun == 5), None)
    player = next((player for player in player_order if player_order_trun.name_room == player['name_room']), None)

    player["GameRound"] += 1

    print(player["GameRound"])
    playerDatabase = await database_sync_to_async(Player.objects.get)(id=player_order_trun.player_id)
    playerDatabase.prise -= room.bet
    room.bank += room.bet

    room.bet = room.bet * 2

    await database_sync_to_async(room.save)()
    await database_sync_to_async(playerDatabase.save)()
    number = (player['number'] + 1) % number_player or number_player

    playerTrun = next((p for p in player_order if number == p['number']), None)

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
        p.trun = 5 if p.name_room == playerTrun['name_room'] else 6

        bet = room.bet / 2 if room.bleackMove and playerTrun['bleack'] else room.bet

        apdateTable = {
            'type': 'apdateTable',
            'bet': bet,
            'bank': room.bank
        }

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
