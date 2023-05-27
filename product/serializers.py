from rest_framework import serializers
from .models import Product
from user.models import Comment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ("id", "name", "available_count", "hidden", "rate", "price", "photo")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ("user", "product", "comment", "rate")