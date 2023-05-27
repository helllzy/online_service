from django.db import models
from django.contrib.auth.models import AbstractUser
import sys
sys.path.append("..product.models")
from product.models import Product


class User(AbstractUser):
    # username
    photo = models.ImageField(blank=True)
    email = models.EmailField(max_length=50)
    bought_prods = models.ManyToManyField(Product, related_name='bought_products')
    created_prods = models.ManyToManyField(Product, related_name='created_products')

    class Meta(AbstractUser.Meta):
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    photo = models.ImageField(blank=True)
    rate = models.IntegerField()

    def __str__(self) -> str:
        return self.comment


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Histories'
 

class HistoryRow(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_count = models.IntegerField()