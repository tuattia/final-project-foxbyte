from rest_framework import serializers
from .models import Product,Transaksi,Quantity

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'harga',
            'stock'
        ]

class TransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        
        fields = [
            'id',
            'created'
        ]

class TransaksiManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        
        fields = [
            'id',
            'product',
            'transaksi',
            'quantity'
        ]


class TransaksiDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Quantity
        fields = [
            'product',
            'quantity'
        ]

class TransaksiShowSerializer(serializers.ModelSerializer):
    transaksi = TransaksiDetailSerializer(many=True, source="related_transaksi")
    
    class Meta:
        model = Transaksi
        fields = [
            'id',
            'created',
            'transaksi',
        ]
