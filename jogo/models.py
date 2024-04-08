from django.db import models


class Jogo(models.Model):
    jogador1 = models.CharField(max_length=255)
    jogador2 = models.CharField(max_length=255)
    venc = models.CharField(max_length=255)
    datahora = models.DateTimeField(auto_now_add=True)
