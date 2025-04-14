from channels.db import database_sync_to_async
from durack_cards.models import Room



async def trun_whipped(self, room_id, number):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    order = room.player_order
    two_player = ''
    number = int(number)

    def_player = next((player.name_room for player in players if player.trun == 2), None)

    if number > 2:
        for player in players:
            if player.name_room == def_player:
                player_status = 1
            else:         
                player_status = 2
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

    else:
        for player in players:
            player_status = 4 
            if player.name_room == def_player:
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















    # if first_player:
    #     index = next((i for i, o in enumerate(order) if o['name_room'] == first_player), None)

    #     if index is not None:
    #         two_player = order[(index + 1) % len(order)]['name_room']
    

    # for player in players:
    #     player_status = 3 
    #     if player.name_room == first_player:
    #         player_status = 1 
    #     elif player.name_room == two_player:
    #         player_status = 2
        
    #     player.trun = player_status
    #     await database_sync_to_async(player.save)()
        
    #     player_message = {
    #         'type': 'playerStatus',
    #         'playerStatus': player_status
    #     } 
    #     await self.channel_layer.send(
    #         player.name_room,
    #         {
    #             'type': 'message',
    #             'message': player_message
    #         }
    #     )

