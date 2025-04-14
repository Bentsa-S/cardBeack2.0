from channels.db import database_sync_to_async
from durack_cards.models import Room
import json



async def to_choose_cards(self, room_id, event):
    number = event['numberCard']
    cards = []
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    card_images = room.cards
    last_card = True
    this_last = None

    for _ in range(min(number, len(card_images))):
        card = card_images.pop()
        if not card_images and last_card:
            this_last = self.channel_name
        cards.append(card)

    cardsAudit = {
        'type': 'cards',
        'cards': cards
    }
    await self.send(text_data=json.dumps({
        'message': cardsAudit
    }))

    if not card_images and last_card:
        last_card = False
        player = next((p for p in players if p.name_room == this_last), None)


        if player:

            await self.send(text_data=json.dumps({
                'message': {
                    'type': 'giveMeLastCard',
                    'id': player.player_id
                }
            }))

            add_last_card = {
                'type': 'addLastCard',
                'id': player.player_id
            }
            for other_player in players:
                if other_player.name_room != this_last:
                    await self.channel_layer.send(
                        other_player.name_room,
                        {
                            "type": "message",
                            "message": add_last_card
                        }
                    )

    room.cards = card_images
    await database_sync_to_async(room.save)()
