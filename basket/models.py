from django.db import models
import sys
sys.path.append("..user.models")
sys.path.append("..product.models")
from user.models import User
from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    general_price = models.FloatField(default=0.0)


class BasketRow(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_count = models.IntegerField()