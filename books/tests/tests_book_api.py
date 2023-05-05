from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse_lazy("books:book-list")


def sample_book(**params) -> Book:
    defaults = {
        "title": "title",
        "author": "author",
        "cover": "H",
        "inventory": 100,
        "daily_fee": 25,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_requirement(self):
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_book(self):
        sample_book()

        response = self.client.get(BOOK_URL)

        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book_detail_forbidden(self):
        book = sample_book()
        url = reverse("books:book-list") + f"{book.pk}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_not_allowed(self):
        book = sample_book()
        url = reverse("books:book-list") + f"{book.pk}/"

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@admin.com",
            "test12345",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_book_create(self):
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": "H",
            "inventory": 25,
            "daily_fee": 100,
        }

        response = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload["title"], getattr(book, "title"))
        self.assertEqual(payload["author"], getattr(book, "author"))

    def test_book_update(self):
        data = {
            "title": "Test",
            "author": "Test",
            "cover": "H",
            "inventory": 250,
            "daily_fee": 50,
        }
        book = sample_book()
        url = reverse("books:book-list") + f"{book.pk}/"

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = sample_book()
        url = reverse("books:book-list") + f"{book.pk}/"

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
