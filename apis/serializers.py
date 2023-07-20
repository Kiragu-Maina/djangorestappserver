from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Products, Product, Shop

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
        fields = ('image', 'title', 'subtitle', 'description','quantity', 'location', 'category', 'shop_name', 'price')
    def get_shop_name(self, obj):
        if obj.shop:
            return obj.shop.shopname
        return None
    

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('shop_owner', 'shopname', 'location', 'phone_no', 'email')
    def create(self, validated_data):
        shop = Shop.objects.create(
            shop_owner=validated_data['shop_owner'],
            shopname=validated_data['shopname'],
            location=validated_data['location'],
            phone_no=validated_data['phone_no'],
            email=validated_data['email']
        )
        return shop