from channels.db import database_sync_to_async
from durack_cards.models import Room, Player
import json


async def add_cards_to_player(self, room_id):
    room = await database_sync_to_async(Room.objects.get)(id=room_id)
    players = await database_sync_to_async(list)(room.players.all())
    cards_to_deal = 6
    players_with_trump = []

    rank_order = {
        '6': 0, '7': 1, '8': 2, '9': 3, '10': 4,
        'J': 5, 'Q': 6, 'K': 7, 'A': 8
    }

    all_cards = room.cards


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

            if(i == 5):
                trump = all_cards[0]
                trump_cards = [card for card in player_cards if card.split('-')[1] == trump.split('-')[1]]
                if trump_cards:
                    min_trump_card = min(trump_cards, key=lambda card: rank_order[card.split('-')[0]])
                    players_with_trump.append((player.name_room, min_trump_card))

        cards = {
            'type': 'cards',
            'cards': player_cards
        }

        await database_sync_to_async(room.save)()

        await self.channel_layer.send(
            player.name_room,
            {
                'type': 'message',
                'message': cards
            }
        )
        await database_sync_to_async(room.save)()
    players_with_trump.sort(key=lambda x: rank_order[x[1].split('-')[0]])
    first_player = players_with_trump[0][0]

    two_player = ''
    for i in range(len(players)):
        if room.player_order[i]['name_room'] == first_player:
            next_index = (i + 1) % len(room.player_order)
            two_player = room.player_order[next_index]['name_room']
    for player in players:
        player_status = 3 
        if player.name_room == first_player:
            player_status = 1 
        elif player.name_room == two_player:
            player_status = 2
        else:
            player_status = 3
        
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

