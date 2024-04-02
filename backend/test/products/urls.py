from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListCreateApiView.as_view(), name="product-create-list"),
    path("<int:pk>/update/", views.ProductUpdateApiView.as_view(), name="product-detail"),
    path("<int:pk>/delete/", views.ProductDeleteApiView.as_view(), name="product-detail"),
    path("<int:pk>", views.ProductDetailApiView.as_view(), name="product-detail"),
]