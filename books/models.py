from django.db import models
from moneyfield import MoneyField

COVER_CHOICES = (
    ("H", "HARD"),
    ("S", "SOFT"),
)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=1,
        choices=COVER_CHOICES,
        default="H",
    )
    inventory = models.PositiveIntegerField()
    daily_fee = MoneyField(
        decimal_places=2,
        max_digits=8,
        currency_default="USD",
    )
