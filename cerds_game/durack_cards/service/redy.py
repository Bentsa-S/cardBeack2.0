from channels.db import database_sync_to_async
from durack_cards.models import Room, Player
import json

async def redy(self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    for p in players:
        if p.name_room == self.channel_name:
            p.redy = True
            await database_sync_to_async(p.save)()

        if p.redy:
            for p in players:
                if p.name_room == self.channel_name:
                    messageName = {
                        'type': 'redy_player',
                        'name': p.name
                    }
                    await self.send(text_data=json.dumps({
                        'message': messageName
                    }))
    
async def check_redy(self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    i = 0

    for p in players:
        if p.redy:
            i += 1
        else:
            break
    
    if len(players) == i:
        messageName = {
            'type': 'redy',
        }

        for p in players:
            if p.name_room != self.channel_name:
                await self.channel_layer.send(
                    p.name_room,
                    {
                        'type': 'message',
                        'message': messageName
                    }
                )
        return True
    else:
        return False
