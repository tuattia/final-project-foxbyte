from rest_framework.views import APIView
from django.http import JsonResponse
from ..models import Transaksi, Quantity, Product
from ..serializer import TransaksiSerializer,TransaksiManageSerializer, TransaksiShowSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated

class TransaksiList(APIView):
    permission_classes = [IsAuthenticated]    

    # Get all data transaksi
    def get(self, request):
        obj = Transaksi.objects.all()
        serializer = TransaksiShowSerializer(obj, many=True)

        return JsonResponse({
            'error': False,
            'data' : serializer.data
        })
    
    def post(self, request):
        body = request.data
        payload_data = []

        # Create transaksi
        transaksiSerializer = TransaksiSerializer(data={})
        # Validate if transaksi is valid
        if transaksiSerializer.is_valid():
            transaksiSerializer.save()
            
            # Looping to append data from request to payload_data
            for item in body['data']:
                stock = Product.objects.get(id=item['product_id']).stock
                if item['quantity'] > stock:
                    transaksi = Transaksi.objects.filter(id=transaksiSerializer.data['id'])
                    transaksi.delete()
                    return JsonResponse({
                        'error': True,
                        'message': 'Quantity product is bigger than product'
                    })
                else:
                    payload_data.append({
                        'product': item['product_id'],
                        'quantity': item['quantity'],
                        'transaksi': transaksiSerializer.data['id']
                    })
            
                    serializer = TransaksiManageSerializer(data=payload_data, many=True)
                    
                    # Validate if serializer is valid
                    if serializer.is_valid():
                        serializer.save()
                        
                        update_stock = stock - item['quantity']
                        product = Product.objects.filter(id=item['product_id']).first()
                        ProductSerializers = ProductSerializer(product, data={
                            'name': Product.objects.get(id=item['product_id']).name,
                            'harga': Product.objects.get(id=item['product_id']).harga,
                            'stock': update_stock
                        })

                        if ProductSerializers.is_valid():
                            ProductSerializers.save()
                            return JsonResponse({
                                'error': False,
                                'data': transaksiSerializer.data['id']
                            })
                        else:
                            return JsonResponse({
                                'error': True,
                                'data': ProductSerializers.errors
                            })
                    else:
                        transaksi = Transaksi.objects.filter(id=transaksiSerializer.data['id'])
                        transaksi.delete()
                        return JsonResponse({
                            'error': True,
                            'data': serializer.errors
                        })   
        else:
            return JsonResponse({
                'error': True,
                'data': transaksiSerializer.errors
            })

class TransaksiDetail(APIView):
    permission_classes = [IsAuthenticated]    

    # Get data transaksi by specific id
    def get(self, request, id):
        obj = Transaksi.objects.filter(id=id).first()
        # Validate if transaksi exist
        if obj:
            serializer = TransaksiShowSerializer(obj)
            return JsonResponse({
                'error': False,
                'data' : serializer.data
            })
        else:
            return JsonResponse({
                'error': True,
                'data' : "Transaksi doens't exist"
            })
    
    # Delete transaksi
    def delete(self, request, id):
        obj = Transaksi.objects.filter(id=id).first()
        # Validate if transaksi exist
        if obj:
            obj.delete()
            return JsonResponse({
                'error': False,
                'message' : 'Transaksi deleted successfully'
            })
        else:
            return JsonResponse({
                'error': True,
                'message' : "Transaksi doesn't exist!"
            })

class TransaksiEdit(APIView):
    permission_classes = [IsAuthenticated]   

    # Update quantity product of transaction
    def put(self, request, id):
        body = request.data
        transaksiObj = Quantity.objects.filter(transaksi=id)
        
        # Validate if id transaksi exist
        if transaksiObj.exists():
            existProduct = transaksiObj.filter(product=body['product_id'])
            # Validate if request product_id exist on transaksi
            if existProduct:
                existProduct.update(quantity=body['quantity'])
                return JsonResponse({
                    'error': False,
                    'messaage': "Update transaksi successfully"
                })
            else:
                return JsonResponse({
                    'error': True,
                    'message': "Product from transaksi doesn't exist"
                })
        else:
            return JsonResponse({
                'error': True,
                'messaage': "Transaksi doesn't exist!"
            })
    
    # Delete product in transaksi
    def delete(self, request, id):
        body = request.data
        transaksiObj = Quantity.objects.filter(transaksi=id)
        
        transaksiObj.filter(product=body['product_id']).delete()

        return JsonResponse({
            'error': False,
            'messaage': "Delete product from transaksi successfully"
        })