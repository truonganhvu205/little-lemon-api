from rest_framework import serializers
import bleach
from .models import Category, MenuItems, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ['id', 'slug', 'title']

class MenuItemsSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    def validate_title(self, value):
        return bleach.clean(value)

    class Meta:
        model = MenuItems
        fields= ['id', 'title', 'price', 'feature', 'category', 'category_id']

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields= ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price']

class Delivery_crew_username(serializers.ModelSerializer):
    class Meta:
        pass

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields= ['id', 'order', 'menuitems', 'quantity', 'unit_price', 'price']

class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']