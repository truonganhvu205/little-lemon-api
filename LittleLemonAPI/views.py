from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Category, MenuItems, Cart, Order, OrderItem
from .serializers import CategorySerializers, MenuItemsSerializers,\
                        CartSerializers, OrderSerializers, OrderItemSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew
# from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsManager, IsAdminUser]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializers
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']

    def get_permissions(self):
        permission_classes = [IsManager, IsAdminUser]

        if self.request.method == 'GET':
            return []
        elif self.request.method == 'POST':
            permission_classes = [IsManager, IsAdminUser]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    # throttle_classes = [AnonRateThrottle, UserRateThrottle]

    # def get_throttles(self):
    #     if self.action == 'create':
    #         throttle_classes = [UserRateThrottle]
    #     else:
    #         throttle_classes = []
    #     return [throttle() for throttle in throttle_classes]

# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItems.objects.all()
#     serializer_class = MenuItemsSerializers

#     def get_permissions(self):
#         permission_classes = [IsDeliveryCrew, IsManager, IsAdminUser]

#         if self.request.method == 'GET':
#             return [IsAuthenticated()]
#         elif self.request.method == 'POST' \
#                 or self.request.method == 'PUT' \
#                 or self.request.method == 'PATCH' \
#                 or self.request.method == 'DELETE':
#             permission_classes = [IsManager, IsAdminUser]
#         else:
#             permission_classes = [IsAdminUser]

#         return [permission() for permission in permission_classes]

#     throttle_classes = [AnonRateThrottle, UserRateThrottle]

# class CartView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializers

#     def get_permissions(self):
#         if self.request.method == 'GET' \
#                 or self.request.method == 'POST' \
#                 or self.request.method == 'DELETE':
#             return [IsAuthenticated()]

#     throttle_classes = [AnonRateThrottle, UserRateThrottle]

# class OrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializers

#     def get_permissions(self):
#         permission_classes = [IsAuthenticated, IsDeliveryCrew, IsManager, IsAdminUser]

#         if self.request.method == 'GET':
#             return []
#         elif self.request.method == 'POST':
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]

#     throttle_classes = [AnonRateThrottle, UserRateThrottle]

# class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializers

#     def get_permissions(self):
#         permission_classes = [IsAuthenticated, IsDeliveryCrew, IsManager, IsAdminUser]

#         if self.request.method == 'GET':
#             return []
#         elif self.request.method == 'PUT' or self.request.method == 'PATCH':
#             permission_classes = [IsAuthenticated]

#             if self.queryset.data:
#                 return JsonResponse(status=1)
#             else:
#                 return JsonResponse(status=0)
#         elif self.request.method == 'PATCH':
#             permission_classes = [IsDeliveryCrew]

#             if self.queryset.data:
#                 return JsonResponse(status=1)
#             else:
#                 return JsonResponse(status=0)
#         return [permission() for permission in permission_classes]

#     throttle_classes = [AnonRateThrottle, UserRateThrottle]