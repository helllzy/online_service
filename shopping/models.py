from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name = models.CharField(max_length=20, blank=False)
    available_count = models.IntegerField(blank=False)
    hidden = models.BooleanField(default=False)
    rate = models.FloatField(default=0.0)
    price = models.FloatField(blank=False)
    photo = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    # username
    bought_prods = models.ManyToManyField(Product, related_name='bought_products')
    created_prods = models.ManyToManyField(Product, related_name='created_products')
    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        return self.username


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='products_to_buy')

    # def __str__(self) -> str:
    #     return self.user
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.product.rate