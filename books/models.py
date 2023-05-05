from django.db import models
from djmoney.models.fields import MoneyField

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
        max_digits=14,
        decimal_places=2,
        default_currency="USD"
    )

    def __str__(self):
        return f"'{self.title}' by {self.author}"
