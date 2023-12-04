from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from rest_framework import generics, status
from .models import Category, MenuItems, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from .serializers import CategorySerializers, MenuItemsSerializers,\
                        CartSerializers, UserSerializers, \
                        OrderSerializers, OrderItemSerializers, OrderPutSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

import math
from datetime import date

# Create your views here.
permission_classes = [IsAdminUser, IsManager, IsDeliveryCrew]

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializers
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsAdminUser | IsManager]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializers

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT' \
                or self.request.method == 'PATCH' \
                or self.request.method == 'DELETE':
            permission_classes = [IsAdminUser | IsManager]
        else:
            permission_classes = [IsAdminUser]
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

    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleManagerUserView(generics.RetrieveDestroyAPIView):
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

    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class DeliveryCrewUserView(generics.ListCreateAPIView):
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

    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleDeliveryCrewUserView(generics.RetrieveDestroyAPIView):
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

    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializers

    def get_queryset(self, *args, **kwargs):
        return Cart.objects.all().filter(user=self.request.user)

    # def post(self, request, *arg, **kwargs):
    #     pass

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response({'Message':'Your items have been deleted.'})

    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializers

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser == True:
            return Order.objects.all()
        elif self.request.user.groups.filter(name='delivery crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        values = cart.values_list()
        if len(values) == 0:
            return HttpResponseBadRequest()
        total = math.fsum([float(values[-1]) for value in values])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for i in cart.values():
            menuitem = get_object_or_404(MenuItems, id=i['menuitem_id'])
            orderitem = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=i['quantity'])
            orderitem.save()
        cart.delete()
        return Response({'Message':'Your order has been placed! Your order number is {}'.format(str(order.id))}, status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST' :
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

# class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = OrderItemSerializers

    def get_queryset(self, *args, **kwargs):
        query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
        return query

    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return Response({'Message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)}, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew']
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return Response({'message':str(crew.username)+' was assigned to order #'+str(order.id)}, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return Response({'message':'Order #{} was deleted'.format(order_number)}, status.HTTP_200_OK)

    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsDeliveryCrew | IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]