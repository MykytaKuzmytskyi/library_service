from django.conf import settings
from django.db import models

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField(blank=True, null=True)
    actual_return_date = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.book} for {self.user}" \
               f" ({self.borrow_date.strftime('%Y.%m.%d %H:%M')})"
