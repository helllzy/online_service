from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name = models.CharField(max_length=20)
    available_count = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    rate = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    photo = models.ImageField()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    # username = models.CharField(max_length=20)
    bought_prods = models.ManyToManyField(Product, related_name='bought_products')
    created_prods = models.ManyToManyField(Product, related_name='created_products')
    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        return self.name


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='products_to_buy')

    def __str__(self) -> str:
        return self.name
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name