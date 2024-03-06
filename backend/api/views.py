from django.http import JsonResponse
from products.serializers import ProductSerializer
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(["GET","POST"])
def api_home(request):
    instance = Product.objects.all().order_by("?").first()
    data={}
    if instance:
        data = ProductSerializer(instance).data
    return Response(data)