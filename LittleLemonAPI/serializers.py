from rest_framework import serializers
import bleach
from .models import Category, MenuItems, Cart, Order, OrderItem

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
    menuitems = MenuItemsSerializers(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields= ['id', 'user', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']
        # user

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        # user, delivery_crew

class OrderItemSerializers(serializers.ModelSerializer):
    menuitems = MenuItemsSerializers(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields= ['id', 'order', 'menuitems', 'quantity', 'unit_price', 'price', 'menuitem_id']
        # order