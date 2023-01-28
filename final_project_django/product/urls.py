from django.urls import path,include
from product import views

urlpatterns = [
    path('product/', views.ProductList.as_view()),
    path('product/<id>', views.ProductDetail.as_view()),
    path('transaksi/', views.TransaksiList.as_view()),
    path('transaksi/<id>', views.TransaksiDetail.as_view()),
    path('transaksi/edit/<id>', views.TransaksiEdit.as_view()),
]