from django.urls import path
from .views import UserAnalyticsView

urlpatterns = [
    path("user-analytics/", UserAnalyticsView.as_view(), name="analytics"),
]
