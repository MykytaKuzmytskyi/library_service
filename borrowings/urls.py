from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingViewSet, BorrowingReturnView

router = routers.DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/return/",
         BorrowingReturnView.as_view(actions={"put": "update"})
         ),
]

app_name = "borrowings"
