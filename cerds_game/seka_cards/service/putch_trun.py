from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json
import random



async def putch_trun (self, room_id, nymber_player, message):
    nymber_player = int(nymber_player)
    message = int(message)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order

    after = room.cards[message + 1:]
    before = room.cards[:message + 1]
    sorted_players = after + before
    await database_sync_to_async(room.save)()

    card = sorted_players.pop()

    player = next((player for player in players if player.trun == 1), None)


    # number = player.number - 1 if player.number > 1 else nymber_player
    

    for p in players:
        # if p.number == number:
        #     p.trun = 3
        # else:
        #     p.trun = 2

        await database_sync_to_async(p.save)()
        
        # player_message = {
        #     'type': 'playerStatus',
        #     'playerStatus': p.trun,
        # } 

        putch_message = {
            'type': 'putch',
            'message': message,
            'card': card,
        }

        # await self.channel_layer.send(
        #     p.name_room,
        #     {
        #         'type': 'message',
        #         'message': player_message
        #     }
        # )

        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': putch_message,
            }
        )

async def putch_start_trun (self, room_id, number_player):
    number_player = int(number_player)
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    player_order = room.player_order


    player_order_trun = next((player for player in players if player.trun == 4), None)
    print(player_order_trun)
    print(players)
    player = next((player for player in player_order if player_order_trun.name_room == player['name_room']), None)

    if number_player == 2:
        number = (player['number'] + 1) % number_player or number_player
    else:
        number = (player['number'] + 2) % number_player or number_player

    playerTrun = next((p for p in player_order if number == p['number']), None)

    for p in players:
        if p.name_room == playerTrun['name_room']:
            p.trun = 5
        else:
            p.trun = 6

        await database_sync_to_async(p.save)()
        
        player_message = {
            'type': 'playerStatus',
            'playerStatus': p.trun,
        } 


        await self.channel_layer.send(
            p.name_room,
            {
                'type': 'message',
                'message': player_message
            }
        )



    