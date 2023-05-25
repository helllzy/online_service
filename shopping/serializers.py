from rest_framework import serializers
from .models import Product, User, Basket, Comment, HistoryRow, BasketRow


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ("id", "name", "available_count", "hidden", "rate", "price", "photo")


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Basket
        fields = ("id", "user", "products")


class BasketRowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BasketRow
        fields = ("product", "prod_count")


class HistoryRowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HistoryRow
        fields = ("product", "prod_count")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ("user", "product", "comment", "rate")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("id", "email", "bought_prods", "created_prods", "username", "photo")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user