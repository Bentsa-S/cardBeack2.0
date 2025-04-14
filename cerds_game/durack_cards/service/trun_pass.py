from channels.db import database_sync_to_async
from durack_cards.models import Room



async def trun_pass(self, room_id, number):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    order = room.player_order
    first_player = next((player.name_room for player in players if player.trun == 2), None)
    number = int(number)
    i = 0

    for player in order:
        if player['name_room'] == self.channel_name:
            player['pass'] = True

    for player in order:
        if player['pass']:
            i += 1
    

    if i == number - 1:
        if first_player:
            index = next((i for i, o in enumerate(order) if o['name_room'] == first_player), None)

            if index is not None:
                two_player = order[(index + 1) % len(order)]['name_room']
        
        for player in players:
            message = {
                "type": 'whipped',
                "id": player.id
            }

            await self.channel_layer.send(
                player.name_room,
                {
                    'type': 'message',
                    'message': message
                }
            )

        for player in players:
            player_status = 3 
            if player.name_room == first_player:
                player_status = 1 
            elif player.name_room == two_player:
                player_status = 2
            
            player.trun = player_status
            await database_sync_to_async(player.save)()
            
            player_message = {
                'type': 'playerStatus',
                'playerStatus': player_status
            } 
            await self.channel_layer.send(
                player.name_room,
                {
                    'type': 'message',
                    'message': player_message
                }
            )


    if i == number - 1:
        for player in order:
            player['pass'] = False

    await database_sync_to_async(Room.objects.filter(id=room_id).update)(player_order=order)



