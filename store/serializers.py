from rest_framework import serializers
from .models import Category, Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock']

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_amount', 'created_at']
        read_only_fields = ['user', 'total_amount']

    def validate_products(self, products):
        # Check stock availability for each product
        for product in products:
            if product.stock < 1:
                raise serializers.ValidationError(f"The product '{product.name}' is out of stock.")
        return products

    def create(self, validated_data):
        products = validated_data.pop('products')
        total_amount = sum([product.price for product in products])
        
        # Create the Order instance with computed total_amount
        order = Order.objects.create(total_amount=total_amount, **validated_data)

        # Add products to order and update stock
        for product in products:
            order.products.add(product)
            product.stock -= 1
            product.save()

        return order
