import json
from channels.db import database_sync_to_async
from durack_cards.models import Room, Player

async def restart(self, room_id, number_player):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    player_order = room.player_order
    number_player = int(number_player)

    players = await database_sync_to_async(lambda: list(room.players.all()))()

    for player in player_order:
        player.update({"trun": 0, "pass": False, "bleack": True, "GameRound": 0})
    room.player_order = player_order
    await room.ensure_cards()

    print(room.cards)
    await database_sync_to_async(room.save)()

    for p in players:
        p.redy = False
        p.trun = 0
        await database_sync_to_async(p.save)()

        restart_msg = {'type': 'restart'}
        await self.channel_layer.send(
            p.name_room, {
                'type': 'message',
                'message': restart_msg
            }
        )
