from rest_framework import serializers
from .models import Product, User, Basket, Comment 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ("id", "name", "available_count", "hidden", "rate", "price", "photo")


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Basket
        fields = ("id", "user", "products")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields =("user", "product", "comment")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("id", "email", "bought_prods", "created_prods", "username")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user