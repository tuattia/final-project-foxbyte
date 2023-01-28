from django.shortcuts import render
from rest_framework.views import APIView
from ..models import Product,Transaksi
from ..serializer import ProductSerializer
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProductList(APIView):
    permission_classes = [IsAuthenticated]
    
    # Get all product
    def get(self, request):
        product = Product.objects.all()

        # conditioning search name product
        if request.GET.get('name') is not None and request.GET.get('name') != "":
          product =  Product.objects.all().filter(name__contains = request.GET.get('name'))
        
        # conditioning search stock product
        if request.GET.get('stock') is not None and request.GET.get('stock') != "":
          product =  Product.objects.filter(stock__gte = request.GET.get('stock'))

        serializer = ProductSerializer(product, many=True)

        return JsonResponse({
                'error': False,
                'data' : serializer.data,
            })

    # Store product
    def post(self, request):
        body = request.data
        
        # product = Product.objects
        serializer = ProductSerializer(data={
            'name': body['name'],
            'harga': body['harga'],
            'stock': body['stock'],
        })
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'error': False,
                'data' : serializer.data,
                'message': "Data saved successfully"
            })
        else:
            return JsonResponse({
                'error': True,
                'data' : None,
                'message': serializer.errors
            })

class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    # Get product by specific id
    def get(self, request, id):
        product = Product.objects.filter(id=id).first()
        serializer = ProductSerializer(product)

        if product:
            return JsonResponse({
                'error': False,
                'data' : serializer.data,
                'message': "Data saved successfully"
            })
        else:
            return JsonResponse({
                'error': True,
                'data' : None,
                'message': "Product doesn't exist!"
            })
        
    # Update product by specific id
    def put(self, request, id):
        payload = request.data
        
        product = Product.objects.filter(id=id).first()

        if product:
            serializer = ProductSerializer(product, data={
                'name': payload['name'],
                'harga': payload['harga'],
                'stock': payload['stock'],
            })
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'error': False,
                    'data' : serializer.data,
                    'message': "Data update successfully"
                })
            else:
                return JsonResponse({
                    'error': True,
                    'data' : None,
                    'message': serializer.errors
                })
        else:
            return JsonResponse({
                'error': True,
                'data' : None,
                'message': "Product doesn't exist!"
            })

    # Delete product by id
    def delete(self, request, id):
        product = Product.objects.filter(id=id).first()
        if product:
            product.delete()
            return JsonResponse({
                'error': False,
                'message': "Data delete successfully"
            })
        else:
            return JsonResponse({
                'error': True,
                'message': "Product doesn't exist!"
            })