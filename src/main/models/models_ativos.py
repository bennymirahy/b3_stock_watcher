from django.contrib.auth.models import User
from django.db import models
from django_qserializer import SerializableManager


class Ativo(models.Model):
    objects = SerializableManager()

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sigla = models.CharField(max_length=16)
    ref_price = models.DecimalField(max_digits=12, decimal_places=3)  # R$
    lower_limit = models.IntegerField()  # Percent
    upper_limit = models.IntegerField()  # Percent
    interval = models.IntegerField()   # Minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'sigla'], name='unique_asset')
        ]


class AtivoHistory(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    close_price = models.DecimalField(max_digits=12, decimal_places=3)  # R$
    timestamp = models.IntegerField()  # Unix timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ativo', 'timestamp'], name='unique_history')
        ]
