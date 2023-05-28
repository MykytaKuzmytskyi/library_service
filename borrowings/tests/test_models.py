from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from books.tests.tests_book_api import sample_book
from borrowings.models import Borrowing


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_borrowing_str(self):
        book = sample_book()
        borrowing = Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=book,
            user=self.user,
        )

        self.assertEqual(
            str(borrowing), f"{borrowing.book} for {borrowing.user}"
                            f" ({borrowing.borrow_date.strftime('%Y.%m.%d %H:%M')})"
        )
