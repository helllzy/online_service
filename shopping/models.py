from django.db import models
from django.contrib.auth.models import AbstractUser

class Product(models.Model):
    name = models.CharField(max_length=20)
    available_count = models.IntegerField()
    hidden = models.BooleanField(default=False)
    rate = models.FloatField(default=0.0)
    price = models.FloatField()
    photo = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.name


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


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    general_price = models.FloatField(default=0.0)


class BasketRow(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_count = models.IntegerField()