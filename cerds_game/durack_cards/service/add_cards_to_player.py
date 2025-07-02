from channels.db import database_sync_to_async
from durack_cards.models import Room, Player
from django.db import transaction
import json


async def add_cards_to_player(self, room_id):
    @database_sync_to_async
    def deal_cards_atomic():
        with transaction.atomic():
            room = Room.objects.select_for_update().get(id=room_id)
            players = list(room.players.all())
            cards_to_deal = 6
            players_with_trump = []

            rank_order = {
                '6': 0, '7': 1, '8': 2, '9': 3, '10': 4,
                'J': 5, 'Q': 6, 'K': 7, 'A': 8
            }

            all_cards = room.cards
            dealt_cards = {}  # Зберігаємо карти для кожного гравця

            for player in players:
                player_cards = []
                for i in range(cards_to_deal):
                    if all_cards:
                        card = all_cards.pop()
                        player_cards.append(card)
                    else:
                        return None, None, None  # Повертаємо None якщо недостатньо карт

                    if(i == 5):
                        trump = all_cards[0]
                        trump_cards = [card for card in player_cards if card.split('-')[1] == trump.split('-')[1]]
                        if trump_cards:
                            min_trump_card = min(trump_cards, key=lambda card: rank_order[card.split('-')[0]])
                            players_with_trump.append((player.name_room, min_trump_card))

                dealt_cards[player.name_room] = player_cards

            room.cards = all_cards
            room.save()

            # Визначаємо першого та другого гравця
            players_with_trump.sort(key=lambda x: rank_order[x[1].split('-')[0]])
            first_player = players_with_trump[0][0] if players_with_trump else None

            two_player = ''
            if first_player:
                for i in range(len(room.player_order)):
                    if room.player_order[i]['name_room'] == first_player:
                        next_index = (i + 1) % len(room.player_order)
                        two_player = room.player_order[next_index]['name_room']

            # Оновлюємо статуси гравців
            for player in players:
                if player.name_room == first_player:
                    player.trun = 1
                elif player.name_room == two_player:
                    player.trun = 2
                else:
                    player.trun = 3
                player.save()

            return dealt_cards, first_player, two_player

    # Виконуємо атомарну операцію
    dealt_cards, first_player, two_player = await deal_cards_atomic()

    if dealt_cards is None:
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': 'Not enough cards in the deck.'
        }))
        return

    # Надсилаємо карти гравцям
    for name_room, cards in dealt_cards.items():
        cards_message = {
            'type': 'cards',
            'cards': cards
        }
        await self.channel_layer.send(
            name_room,
            {
                'type': 'message',
                'message': cards_message
            }
        )

        # Надсилаємо статус гравця
        player_status = 1 if name_room == first_player else (2 if name_room == two_player else 3)
        player_message = {
            'type': 'playerStatus',
            'playerStatus': player_status
        }
        await self.channel_layer.send(
            name_room,
            {
                'type': 'message',
                'message': player_message
            }
        )

