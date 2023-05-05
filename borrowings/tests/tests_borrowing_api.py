from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.tests.tests_book_api import sample_book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer

BORROWING_URL = reverse_lazy("borrowings:borrowing-list")


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_requirement(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_borrowings_are_available_only_for_authenticated_users(self):
        data = {
            "expected_return_date": timezone.now(),
            "book": sample_book(),
        }
        response = self.client.post(BORROWING_URL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_one = get_user_model().objects.create_user(
            "first@test.com",
            "test12345",
        )
        self.user_two = get_user_model().objects.create_user(
            "second@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user_one)
        book = sample_book()
        borrowing1 = Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=book,
            user=self.user_one,
        )
        borrowing2 = Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=book,
            user=self.user_two,
        )

    def test_non_admins_can_see_only_their_borrowings(self):
        response = self.client.get(BORROWING_URL)
        borrowing = Borrowing.objects.filter(user=self.user_one)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(borrowing))

    def test_borrowing_create(self):
        data = {
            "expected_return_date": datetime.now(),
            "book": 1,
        }
        response = self.client.post(BORROWING_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AdminBorrowingApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user_admin = get_user_model().objects.create_user(
            "test@admin.com",
            "testpass",
            is_staff=True
        )
        self.user_one = get_user_model().objects.create_user(
            "first@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user_admin)

        book1 = Book.objects.create(
            title="Test book",
            author="Test author",
            cover="H",
            inventory=10,
            daily_fee=10,
        )
        book2 = sample_book(title="Book2")

        Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=book1,
            user=self.user_admin,
        )
        Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=book2,
            user=self.user_one,
            actual_return_date=timezone.now(),
        )

    def test_borrowing_return(self):
        data = {
            "actual_return_date": datetime.now(),
        }
        borrowing = Borrowing.objects.get(pk=1)
        url = reverse("borrowings:borrowing-list") + f"{borrowing.pk}/return/"
        response = self.client.put(url, data, )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_return_borrowing_twice(self):
        data = {
            "actual_return_date": timezone.now(),
            "user": 1,
        }

        borrowing = Borrowing.objects.get(user=self.user_admin)
        url = reverse("borrowings:borrowing-list") + f"{borrowing.pk}/return/"

        response1 = self.client.put(url, data)
        response2 = self.client.put(url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_borrowings_by_is_active(self):
        borrowing_is_active = Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=sample_book(),
            user=self.user_admin,
        )
        borrowing_is_not_active = Borrowing.objects.create(
            expected_return_date=timezone.now(),
            book=sample_book(),
            actual_return_date=timezone.now(),
            user=self.user_admin,
        )
        url = reverse("borrowings:borrowing-list") + "?is_active"
        response = self.client.get(BORROWING_URL)
        response_is_active = self.client.get(url)

        serializer = BorrowingListSerializer(borrowing_is_not_active)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_is_active.status_code, status.HTTP_200_OK)

        self.assertNotEqual(response.data, response_is_active.data)
        self.assertIn(serializer.data, response.data)
        self.assertNotIn(serializer.data, response_is_active.data)

    def test_filter_borrowings_by_user_id(self):
        res = self.client.get(BORROWING_URL, {"user_id": f"{self.user_admin.pk}"})
        borrowing1 = Borrowing.objects.get(user=self.user_admin)
        borrowing2 = Borrowing.objects.get(user=self.user_one.pk)
        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
