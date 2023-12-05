from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
import bleach
from decimal import Decimal

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ['id', 'title', 'slug']

class MenuItemSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    def validate_title(self, value):
        return bleach.clean(value)

    class Meta:
        model = MenuItem
        fields= ['id', 'title', 'price', 'feature', 'category', 'category_id']

class CartSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields= ['id', 'user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price':{'read_only':True}
        }

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= ['id', 'order', 'menuitem', 'quantity', 'price']

class OrderSerializers(serializers.ModelSerializer):
    orderitem = OrderItemSerializers(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'orderitem']

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']