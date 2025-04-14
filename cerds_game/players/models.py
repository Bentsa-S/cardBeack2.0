from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField(default=0)
    prise = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.name

    def add_friend(self, friend_user_id):
        try:
            friend = Player.objects.get(user_id=friend_user_id)
            print(friend)
            if friend != self and not self.friends.filter(id=friend.id).exists():
                self.friends.add(friend)
                return True
            return False
        except Player.DoesNotExist:
            return False

    def remove_friend(self, friend_user_id):

        friend = Player.objects.get(user_id=friend_user_id)
        if friend in self.friends.all():
            self.friends.remove(friend)
            return True
        return False
