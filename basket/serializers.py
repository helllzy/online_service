from rest_framework import serializers
from .models import Basket, BasketRow


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Basket
        fields = ("id", "user", "products")


class BasketRowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BasketRow
        fields = ("product", "prod_count")