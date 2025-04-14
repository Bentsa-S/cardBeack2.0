import json
from channels.db import database_sync_to_async
from seka_cards.models import Room, Player

async def restart(self, room_id, number_player, bet):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)

    # Якщо це JSONField, зміни збережуться автоматично
    player_order = room.player_order
    player_cards_order = room.player_cards_order

    number_player = int(number_player)
    players = await database_sync_to_async(lambda: list(room.players.all()))()

    pass_count = sum(1 for p in player_order if isinstance(p, dict) and p.get('pass'))
    print(pass_count)

    room.bet = bet
    room.bank = 0

    for player in player_order:
        player.update({"trun": 0, "pass": False, "bleack": True, "GameRound": 0})

    for player in player_cards_order:
        player["cards"] = []

    room.player_order = player_order
    room.player_cards_order = player_cards_order

    await database_sync_to_async(room.save)()

    print(room.player_order)
    print(player_order)
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
