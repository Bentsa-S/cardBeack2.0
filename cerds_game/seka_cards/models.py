from django.db import models
from channels.db import database_sync_to_async
import random


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    participants = models.PositiveIntegerField(default=2)
    deck = models.PositiveIntegerField(default=0)
    rate = models.FloatField(default=0)
    bet = models.PositiveIntegerField(default=0)
    bank = models.PositiveIntegerField(default=0)
    isPrivate = models.BooleanField(default=False)
    password = models.PositiveIntegerField(default=0)
    hew = models.BooleanField(default=False)
    push = models.BooleanField(default=False)
    cards = models.JSONField(default=list)
    bleackMove = models.BooleanField(default=False)
    # seven = models.BooleanField(default=False)
    player_order = models.JSONField(default=list)
    player_cards_order = models.JSONField(default=list)


    def __str__(self):
        return f"Room {self.id}"

    @database_sync_to_async
    def ensure_cards(self):
        if not self.cards:
            all_cards = [
                "7-Hearts", "10-Clubs", "10-Diamonds", "10-Hearts", "10-Spades", 
                "A-Clubs", "A-Diamonds", "A-Hearts", "A-Spades", "J-Clubs", 
                "J-Diamonds", "J-Hearts", "J-Spades", "K-Clubs", "K-Diamonds", 
                "K-Hearts", "K-Spades", "Q-Clubs", "Q-Diamonds", "Q-Hearts", "Q-Spades"
            ]
            random.shuffle(all_cards)
            self.cards = all_cards
            self.save()  # Save the cards list
        else:
            print(f"Cards already initialized for room {self.id}")

    @database_sync_to_async
    def add_player(self, name, name_room, trun, player_id, redy=False):
        # Перевірка чи гравець з таким player_id вже існує
        player = Player.objects.filter(room=self, player_id=player_id).first()
        
        if player:
            # Якщо гравець з таким player_id існує, оновлюємо його дані
            player.name = name
            player.trun = trun
            player.redy = redy
            player.name_room = name_room
            player.save()
        else:
            # Якщо гравець не існує, створюємо нового
            player = Player.objects.create(
                room=self,
                name=name,
                trun=trun,
                redy=redy,
                name_room=name_room,
                player_id=player_id
            )
            player.save()

        return player

class Player(models.Model):
    room = models.ForeignKey(Room, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    trun = models.IntegerField()
    redy = models.BooleanField()
    name_room = models.CharField(max_length=100, default='default_room')  # Set a default value
    player_id = models.IntegerField()

    def __str__(self):
        return self.name

