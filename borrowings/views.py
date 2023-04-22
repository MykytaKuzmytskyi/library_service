from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer, BorrowingCreateSerializer
)


class BorrowingViewSet(ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer


class BorrowingCreateViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer

