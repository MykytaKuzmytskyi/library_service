from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer, BorrowingReturnSerializer
)
from borrowings.tasks import send_telegram


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        book = Book.objects.get(id=self.request.data["book"])
        book.inventory -= 1
        book.save()
        try:
            send_telegram.delay(f"{book.title} borrowed by {self.request.user}")
        except ValueError:
            print("Message was not sent!"
                  "'chat_id' or 'token' data is not correct.")

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        if is_active is not None and self.request.user.is_authenticated:
            queryset = queryset.filter(actual_return_date=None)

        if user_id is not None and self.request.user.is_superuser:
            user_ids = self._params_to_ints(user_id)
            queryset = queryset.filter(user__id__in=user_ids)

        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        return BorrowingListSerializer

    @action(
        methods=["PUT"],
        detail=True,
        url_path="return",
        permission_classes=[IsAdminUser]
    )
    def return_borrowing(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
        borrowing = self.get_object()
        serializer = self.get_serializer(
            borrowing, data=request.data, partial=partial
        )
        if serializer.is_valid(raise_exception=True):
            borrowing.book.inventory += 1
            borrowing.book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
