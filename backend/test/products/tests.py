from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
# Create your tests here.


class TestProductApi(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Product.objects.create(title="First Product", content="First Content", price=100)
    def test_product_detail(self):
        url = reverse("product-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_404(self):
        url = reverse("product-detail", args=[1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
