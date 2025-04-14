from channels.db import database_sync_to_async
from seka_cards.models import Room
from players.models import Player
import json



async def bleack_flip (self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    player_order = room.player_order
    player = next((p for p in player_order if self.channel_name == p['name_room']), None)

    player['bleack'] = False

    await database_sync_to_async(room.save)()
    if not room.bleackMove:
        bet = room.bet / 2
    else:
        bet = room.bet

    playerBlaeck = {
        'type': 'cardFlip'
    }

    apdateTable = {
        'type': 'apdateTable',
        'bet': bet,
        'bank': room.bank
    } 

    await self.send(text_data=json.dumps(
        {
            'type': 'message',
            'message': playerBlaeck
        }
    ))

    await self.send(text_data=json.dumps(
        {
            'type': 'message',
            'message': apdateTable
        }
    ))
