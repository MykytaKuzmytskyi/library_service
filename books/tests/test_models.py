from django.test import TestCase

from books.models import Book


class ModelsTests(TestCase):
    def test_book_str(self):
        book = Book.objects.create(
            title="Test title",
            author="Test author",
            cover="H",
            inventory=50,
            daily_fee=25,
        )
        self.assertEqual(
            str(book), f"'{book.title}' by {book.author}"
        )
