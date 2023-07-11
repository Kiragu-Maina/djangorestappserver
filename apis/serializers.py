from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Products, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'itemName', 'description', 'price', 'quantity', 'image']

class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('image', 'title', 'subtitle', 'description', 'location', 'category', 'shop_name', 'price')
    def get_shop_name(self, obj):
        if obj.shop:
            return obj.shop.shopname
        return None