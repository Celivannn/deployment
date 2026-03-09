from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Category, Product
from orders.models import Cart, CartItem, Order, OrderItem
from analytics.models import SalesAnalytics, DailyOrderStats, TopProduct

# Enhanced UserSerializer with more fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal', 'created_at']
    
    def get_subtotal(self, obj):
        # Convert Decimal to float for JSON serialization
        return float(obj.quantity * obj.price)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'items', 'total', 'item_count', 'created_at', 'updated_at']
    
    def get_total(self, obj):
        # Calculate total as float
        total = sum(float(item.quantity * item.price) for item in obj.items.all())
        return total
    
    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']
    
    def get_subtotal(self, obj):
        return float(obj.quantity * obj.price)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = UserSerializer(source='user', read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_total_amount(self, obj):
        return float(obj.total_amount)

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_method', 'customer_name', 'customer_phone', 
                 'customer_email', 'special_instructions']

class SalesAnalyticsSerializer(serializers.ModelSerializer):
    total_revenue = serializers.SerializerMethodField()
    average_order_value = serializers.SerializerMethodField()
    
    class Meta:
        model = SalesAnalytics
        fields = '__all__'
    
    def get_total_revenue(self, obj):
        return float(obj.total_revenue)
    
    def get_average_order_value(self, obj):
        return float(obj.average_order_value)