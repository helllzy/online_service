from django.contrib import admin
from .models import Product, User, Basket, Comment

admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Basket)