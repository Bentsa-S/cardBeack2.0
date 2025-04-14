import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .service import add_player_room, remove_player_room, redy, check_redy, add_goat, add_cards_to_player, send_to_others, trun_teka, trun_whipped, to_choose_cards, swap_player_room, trun_pass, check_to_win, restart
from .models import Room, Player

class RyoomCardsGame(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.number_players = self.scope['url_route']['kwargs']['number_players']

        # Перевірка на наявність кімнати
        if not await self.room_exists(self.room_id):
            await self.close()
            return
        

        self.room = await self.get_room(self.room_id)

        self.group_name = f"group_{self.room_id}"

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.room.ensure_cards()
    async def receive(self, text_data):

        json_data = json.loads(text_data)
        action = json_data.get('type')
        if action == 'user':
            await add_player_room(self, json_data, self.room_id, self.number_players)
        if action == 'swap':
            await swap_player_room(self, self.room_id, json_data.get('number'))
        if action == 'redy':
            # await self.delete_all_players()
            await redy(self, self.room_id)

            if await check_redy(self, self.room_id):
                await add_goat(self, self.room_id)
                await add_cards_to_player(self, self.room_id) # end create to trum
        if action == 'audit':
            await to_choose_cards(self, self.room_id, json_data)
        if action == 'teka':
            await trun_teka(self, self.room_id)
            await send_to_others(self, self.room_id, json_data)
        if action == 'whipped':
            await trun_whipped(self, self.room_id, self.number_players)
            # await send_to_others(self, self.room_id, json_data)
        if action == 'pass':
            await trun_pass(self, self.room_id, self.number_players)
        if action == 'def' or action == 'atack':
            await send_to_others(self, self.room_id, json_data)
        if action == 'win':
            await check_to_win(self, self.room_id, json_data.get('id'))
        if action == 'restart':
            await restart(self, self.room_id, self.number_players)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await remove_player_room(self, self.room_id)
        await self.remove_player_from_db()
        await self.remove_player_and_check_room(self.room_id)


    @database_sync_to_async
    def remove_player_and_check_room(self, room_id):
        room = Room.objects.get(id=room_id)
        if not room.players.exists():
            room.player_order.clear()
            room.delete()
            

    @database_sync_to_async
    def remove_player_from_db(self):
        player = Player.objects.get(name_room=self.channel_name)
        player.delete()
            
            

    @database_sync_to_async
    def get_or_create_room(self, room_id):
        room, created = Room.objects.get_or_create(id=room_id)
        return room

    @database_sync_to_async
    def delete_all_players(self):
        Player.objects.all().delete()
        self.room.player_order = []  # Присвоюємо порожній список
        self.room.save()  # Зберігаємо зміни до бази даних

    @database_sync_to_async
    def get_room(self, room_id):
        return Room.objects.get(id=room_id)

    @database_sync_to_async
    def room_exists(self, room_id):
        return Room.objects.filter(id=room_id).exists()
    
    async def message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

