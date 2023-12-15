from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from rest_framework import generics, viewsets, status
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializers, MenuItemSerializers,\
                        CartSerializers, OrderSerializers, \
                        OrderItemSerializers, UserSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializers

    search_fields = ['title', 'category__title']
    ordering_fields = ['price']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializers

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class ManagerUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        manager_group = Group.objects.get(name='manager')
        return User.objects.all().filter(groups=manager_group)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.add(user)
            return Response({'Message':'User had been added.'}, status.HTTP_201_CREATED)
        return Response({'Message':'Error.'}, status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleManagerUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        manager_group = Group.objects.get(name='manager')
        return User.objects.all().filter(groups=manager_group)

    def delete(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.remove(user)
            return Response({'Message':'User had been removed.'}, status.HTTP_200_OK)
        return Response({'Message':'Error.'}, status.HTTP_404_NOT_FOUND)

    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class DeliveryCrewUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        delivery_crew_group = Group.objects.get(name='delivery crew')
        return User.objects.all().filter(groups=delivery_crew_group)

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew_group = Group.objects.get(name='delivery crew')
            delivery_crew_group.user_set.add(user)
            return Response({'Message':'User had been added.'}, status.HTTP_201_CREATED)
        return Response({'Message':'Error.'}, status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleDeliveryCrewUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):
        delivery_crew_group = Group.objects.get(name='delivery crew')
        return User.objects.all().filter(groups=delivery_crew_group)

    def delete(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew_group = Group.objects.get(name='delivery crew')
            delivery_crew_group.user_set.remove(user)
            return Response({'Message':'User had been removed.'}, status.HTTP_200_OK)
        return Response({'Message':'Error.'}, status.HTTP_404_NOT_FOUND)

    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

    def get_queryset(self, *args, **kwargs):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response({'Message':'Your items have been deleted.'})

    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count() == 0:
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='delivery crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()

    def post(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({'Message':'No item in cart.'})
        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializers = OrderSerializers(data=data)
        if order_serializers.is_valid():
            order = order_serializers.save()
            items = Cart.objects.all().filter(user=self.request.user).all()
            for item in items.values():
                orderitem = OrderItem(
                    order = order,
                    menuitem_id = item['menuitem_id'],
                    price = item['price'],
                    quantity = item['quantity']
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializers.data.copy()
            result['total'] = total
            return Response(order_serializers.data)

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total

    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count() == 0:
            return Response('Not Ok')
        else:
            return super().update(request, *args, **kwargs)

    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
