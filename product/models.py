from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=20)
    available_count = models.IntegerField()
    hidden = models.BooleanField(default=False)
    rate = models.FloatField(default=0.0)
    price = models.FloatField()
    photo = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.name