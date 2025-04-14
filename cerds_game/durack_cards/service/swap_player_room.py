from channels.db import database_sync_to_async
from durack_cards.models import Room, Player



async def swap_player_room(self, room_id, number_swap):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    order = room.player_order
    player_to_swap = None
    for player in order:
        if player['user']:
            if player['name_room'] == self.channel_name:
                player_to_swap = player
                break

    if player_to_swap:
        updated_order = []
        for player in order:
            if player['number'] == player_to_swap['number']:
                updated_order.append({'user': False, 'number': player_to_swap['number']})
            elif player['number'] == number_swap:
                updated_order.append({'user': True, 'name': player_to_swap['name'], 'name_room': self.channel_name, 'number': number_swap, 'id': player_to_swap['id']})  # Переміщуємо гравця на місце 5
            else:
                updated_order.append(player)

        order = updated_order

    room.player_order = order
    await database_sync_to_async(room.save)()
    
    message = {
        "type": 'swap',
        "swap": order
    }

    for player in order:
        if (player['user']):
            await self.channel_layer.send(
                player['name_room'],
                {
                    "type": "message",
                    "message": message
                }
            )
