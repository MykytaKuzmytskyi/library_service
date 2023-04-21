from django.db import models

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
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)
