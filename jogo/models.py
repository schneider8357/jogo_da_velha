from django.db import models
from django.contrib.auth import get_user_model


class Board(models.Model):
    tile0 = models.CharField(max_length=1, null=True, default=None)
    tile1 = models.CharField(max_length=1, null=True, default=None)
    tile2 = models.CharField(max_length=1, null=True, default=None)
    tile3 = models.CharField(max_length=1, null=True, default=None)
    tile4 = models.CharField(max_length=1, null=True, default=None)
    tile5 = models.CharField(max_length=1, null=True, default=None)
    tile6 = models.CharField(max_length=1, null=True, default=None)
    tile7 = models.CharField(max_length=1, null=True, default=None)
    tile8 = models.CharField(max_length=1, null=True, default=None)

class Jogo(models.Model):
    jogador1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="jogador1_user")
    jogador2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name="jogador2_user")
    venc = models.CharField(max_length=255)
    proximo = models.IntegerField(default=1)
    datahora = models.DateTimeField(auto_now_add=True)
    board = models.OneToOneField(Board, on_delete=models.CASCADE)
    senha = models.CharField(max_length=24, blank=True)
