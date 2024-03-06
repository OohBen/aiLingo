from django.test import TestCase
from django.urls import reverse
from products.models import Product
# Create your tests here.

class BasicTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Product.objects.create(title="ti")
    def test_url_exist(self):
        url = reverse("home")
        self.assertEqual(self.client.get(url).status_code,200)
        print(self.client.get(url).content)