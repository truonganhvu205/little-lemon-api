from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework import generics
from .models import Category, MenuItems, Cart, Order, OrderItem
from django.contrib.auth.models import User
from .serializers import CategorySerializers, MenuItemsSerializers,\
                        CartSerializers, UserSerializers, \
                        OrderSerializers, OrderItemSerializers, OrderPutSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import math
from datetime import date

# Create your views here.
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
        permission_classes = [IsAdminUser, IsManager, IsDeliveryCrew]

        if self.request.method == 'GET':
            return []
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
        permission_classes = [IsAdminUser, IsManager, IsDeliveryCrew]

        if self.request.method == 'GET':
            return []
        elif self.request.method == 'PUT' \
                or self.request.method == 'PATCH' \
                or self.request.method == 'DELETE':
            permission_classes = [IsAdminUser | IsManager]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class ManagerUserView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups=1)
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleManagerUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups=1)
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class DeliveryCrewUserView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups=2)
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class SingleDeliveryCrewUserView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups=2)
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user)
        return cart

    def post(self, request, *arg, **kwargs):
        serialized_item = CartSerializers(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        id = request.data['menuitem']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItems, id=id)
        price = int(quantity) * item.price

        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=price, menuitem_id=id)
        except:
            return JsonResponse(status=409, data={'message':'Item already in cart'})

        return JsonResponse(status=201, data={'message':'Item added to cart!'})

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializers

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Managers').exists() or self.request.user.is_superuser == True :
            query = Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            query = Order.objects.filter(delivery_crew=self.request.user)
        else:
            query = Order.objects.filter(user=self.request.user)
        return query

    def get_permissions(self):
        if self.request.method == 'GET' or 'POST' :
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        x=cart.values_list()
        if len(x) == 0:
            return HttpResponseBadRequest()
        total = math.fsum([float(x[-1]) for x in x])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for i in cart.values():
            menuitem = get_object_or_404(MenuItems, id=i['menuitem_id'])
            orderitem = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=i['quantity'])
            orderitem.save()
        cart.delete()
        return JsonResponse(status=201, data={'message':'Your order has been placed! Your order number is {}'.format(str(order.id))})

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializers

    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticatedOrReadOnly, IsManager | IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, IsDeliveryCrew | IsManager | IsAdminUser]
        return[permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
            query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return query

    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return JsonResponse(status=200, data={'message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)})

    def put(self, request, *args, **kwargs):
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew']
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return JsonResponse(status=201, data={'message':str(crew.username)+' was assigned to order #'+str(order.id)})

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return JsonResponse(status=200, data={'message':'Order #{} was deleted'.format(order_number)})

    throttle_classes = [AnonRateThrottle, UserRateThrottle]