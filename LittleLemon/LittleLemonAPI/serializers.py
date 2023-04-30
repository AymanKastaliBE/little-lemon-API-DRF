from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem, Category
from django.contrib.auth.models import User


class MenuItemSerializer(ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        
    
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        

class CartSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
)
    price = serializers.SerializerMethodField(method_name='calculate_price')
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price'] 
        
    def calculate_price(self, cart:Cart):
        return cart.quantity * cart.unit_price
    
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ManagerOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']

        
class DeliveryCrewOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class CustomerOrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem')
    total = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'date', 'status', 'total', 'order_items']

    def get_total(self, obj:Order):
            total = 0
            for item in obj.orderitem.all():
                total += item.quantity * item.unit_price
            return total


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'