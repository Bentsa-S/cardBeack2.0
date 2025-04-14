from channels.db import database_sync_to_async
from durack_cards.models import Room, Player
import json


async def add_goat(self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    card_images = room.cards
    if card_images:
        last_card = card_images[0]

        message = {
            'type': 'goat',
            'goat': last_card
        }
        # Відправляємо повідомлення всій групі
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'message',
                'message': message
            }
        )
    else:
        # Відправляємо повідомлення про помилку, якщо колода порожня
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'goat_message',
                'message': {'error': 'Deck is empty.'}
            }
        )
