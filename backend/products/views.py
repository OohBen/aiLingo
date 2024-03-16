from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer

class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #Set which fields to be used for creating the new model
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content=title
        serializer.save(content=content)

class ProductListApiView(generics.ListAPIView):
    #Going to use ListCreateAPIView instead of ListAPIView.
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET', 'POST'])

def product_alt_view(request, pk=None, *args, **kwargs):
    if request.method == 'GET':
        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(product).data
            return Response(data)
        
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content=title
            serializer.save(content=content)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)