from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Game(models.Model):
    name=models.CharField(max_length=30, null=False, blank=False, unique=False)
    price = models.FloatField(null=False, blank=False, unique=False)
    url = models.URLField(max_length=300, null=False, blank=False, unique=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

class Transaction(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    paid_amount = models.FloatField()
    timestamp = models.DateField(default=timezone.now)

# Create your models here.
