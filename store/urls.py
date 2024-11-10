from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-detail'),
    path('products/', ProductAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),
    path('orders/', OrderAPIView.as_view(), name='order-list-create'),
]