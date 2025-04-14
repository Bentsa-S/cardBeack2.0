import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .service import add_player_room, pass_trun, redy, swap_player_room, check_redy, remove_player_room, add_cards_to_player, start_trun, putch_trun, take_trun, redy_take_trun, putch_start_trun, play_trun, bleack_move_trun, bleack_flip, up_bet_trun, look_card_trun, restart
from .models import Room, Player
import logging

logger = logging.getLogger(__name__)

class RyoomCardsSeka(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.number_players = self.scope['url_route']['kwargs']['number_players']
        self.bet = self.scope['url_route']['kwargs']['bet']

        if not await self.room_exists(self.room_id):
            await self.close()
            return
        self.room = await self.get_or_create_room(self.room_id)


        self.group_name = f"group_{self.room_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.room.ensure_cards()

        await self.accept()

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        action = json_data.get('type')
        print(action)
        if action == 'user':

            await add_player_room(self, json_data, self.room_id, self.number_players)
        if action == 'swap':
            await swap_player_room(self, self.room_id, json_data.get('number'))
        if action == 'redy':
            # await self.delete_all_players()
            await redy(self, self.room_id)

            if await check_redy(self, self.room_id):
                await start_trun(self, self.room_id, self.number_players)
                # await add_cards_to_player(self, self.room_id)
        if action == 'putch':
            await putch_trun(self, self.room_id, self.number_players, json_data.get('message'))
        if action == 'take':
            await take_trun(self, self.room_id)
        if action == 'redyTake':
            await redy_take_trun(self, self.room_id, self.number_players)
        if action == 'endSwapCards':
            await putch_start_trun(self, self.room_id, self.number_players)
            await add_cards_to_player(self, self.room_id, self.number_players)
        if action == 'play':
            await play_trun(self, self.room_id, self.number_players)
        if action == 'upBetToBleack':
            await bleack_move_trun(self, self.room_id, self.number_players)
        if action == 'flipBleack':
            await bleack_flip(self, self.room_id)
        if action == 'upBet':
            await up_bet_trun(self, self.room_id, self.number_players, json_data.get('bet'))
        if action == 'pass':
            await pass_trun(self, self.room_id, self.number_players, json_data.get('id'))
        if action == 'lookCards':
            await look_card_trun(self, self.room_id, self.number_players, json_data.get('id'))
        if action == 'restart':
            await restart(self, self.room_id, self.number_players, self.bet)

        # if action == 'def' or action == 'atack':
        #     await send_to_others(self, self.room_id, json_data)

    async def disconnect(self, close_code):
        logger.info(f"Disconnect started for room: {self.room_id}, channel: {self.channel_name}")
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            await self.remove_player_from_db()
            await self.remove_player_and_check_room(self.room_id)
            await remove_player_room(self, self.room_id)
            logger.info(f"Successfully disconnected room: {self.room_id} with channel: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error during disconnect: {str(e)}")
    @database_sync_to_async
    def remove_player_and_check_room(self, room_id):
        try:
            room = Room.objects.get(id=room_id)
            logger.info(f"Room found: {room_id}, checking players...")
            
            # Перевірка, чи є гравці в кімнаті
            if not room.players.exists():
                logger.info(f"Room {room_id} is empty, deleting room...")
                room.player_order.clear()
                room.delete()
            else:
                logger.info(f"Room {room_id} has players, not deleting.")
        except Room.DoesNotExist:
            logger.error(f"Room with id {room_id} does not exist.")
            # Можна зробити додаткову обробку помилки, якщо потрібно

    @database_sync_to_async
    def remove_player_from_db(self):
        try:
            player = Player.objects.get(name_room=self.channel_name)
            logger.info(f"Removing player: {player.name_room}")
            player.delete()
        except Player.DoesNotExist:
            logger.error(f"Player with channel name {self.channel_name} does not exist.")
            # Можна зробити додаткову обробку помилки, якщо потрібно

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

