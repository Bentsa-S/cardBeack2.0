from channels.db import database_sync_to_async
from seka_cards.models import Room, Player
import json


async def add_cards_to_player(self, room_id, number_player):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    cards_to_deal = 3
    player_order = room.player_order
    player_cards_order = room.player_cards_order


    player_order_trun = next((player for player in players if player.trun == 5), None)
    index = player_order.index(next(player for player in player_order if player['name_room'] == player_order_trun.name_room))
    room.player_order = player_order[index:] + player_order[:index]

    for i, player in enumerate(room.player_order, start=1):
        player['number'] = i

    await database_sync_to_async(room.save)()

    all_cards = self.room.cards

    for player in players:
        player_cards = []
        for i in range(cards_to_deal):
            if all_cards:
                card = all_cards.pop()
                player_cards.append(card)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Not enough cards in the deck.'
                }))

        cards = {
            'type': 'cards',
            'cards': player_cards,
            'players': room.player_order
        }

        await self.channel_layer.send(
            player.name_room,
            {
                'type': 'message',
                'message': cards
            }
        )

        player_order_trun_cards = next((p for p in player_cards_order if p["name_room"] == player.name_room), None)
        player_order_trun_cards["cards"] = player_cards

        room.player_cards_order = player_cards_order
        await database_sync_to_async(room.save)()
