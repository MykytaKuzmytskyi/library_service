from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
        )

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data["book"].inventory == 0:
            raise serializers.ValidationError("This book is not available.")
        return data


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "actual_return_date",
            "user",
        )

    def validate(self, data):
        """
        Check that start is before finish.
        """
        return_date = self.instance.actual_return_date
        if self.instance.actual_return_date is not None:
            raise serializers.ValidationError(f"This book has been returned {return_date.strftime('%Y.%m.%d %H:%M')}!")
        if data['actual_return_date'] is None:
            raise serializers.ValidationError("Field actual_return_date must not be empty!")
        return data
