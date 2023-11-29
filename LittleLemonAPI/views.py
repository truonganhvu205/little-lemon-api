from django.shortcuts import render
from rest_framework import generics
from .models import Category, MenuItems, Cart, Order, OrderItem
from .serializers import CategorySerializers, MenuItemsSerializers,\
                        CartSerializers, OrderSerializers, OrderItemSerializers

# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializers
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializers