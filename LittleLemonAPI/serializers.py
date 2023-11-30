from rest_framework import serializers
import bleach
from .models import Category, MenuItems, Cart, Order, OrderItem
from django.contrib.auth.models import User

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

class CartSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    menuitems = MenuItemsSerializers(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields= ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']

class OrderSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    class Meta:
        model = Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializers(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    menuitems = MenuItemsSerializers(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields= ['id', 'order', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']