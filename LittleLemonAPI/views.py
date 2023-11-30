from django.shortcuts import render
from rest_framework import generics
from .models import Category, MenuItems, Cart, Order, OrderItem
from .serializers import CategorySerializers, MenuItemsSerializers,\
                        CartSerializers, OrderSerializers, OrderItemSerializers
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# class CategoryView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializers
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return []
        else:
            return [IsAuthenticated()]

    # def get_throttles(self):
    #     if self.action == 'create':
    #         throttle_classes = [UserRateThrottle]
    #     else:
    #         throttle_classes = []
    #     return [throttle() for throttle in throttle_classes]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.select_related('category').all()
    serializer_class = MenuItemsSerializers
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        else:
            return [IsAuthenticated()]

    # def get_throttles(self):
    #     if self.action == 'create'|self.action == 'update'|self.action == 'partial_update'|self.action == 'destroy':
    #         throttle_classes = [UserRateThrottle]
    #     else:
    #         throttle_classes = []
    #     return [throttle() for throttle in throttle_classes]
