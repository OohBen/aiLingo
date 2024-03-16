from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListCreateApiView.as_view(), name="product-create-list"),
    path("<int:pk>", views.ProductDetailApiView.as_view(), name="product-detail"),
]