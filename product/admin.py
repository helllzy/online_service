from django.contrib import admin
from .models import Product
from user.models import Comment

admin.site.register(Comment)
admin.site.register(Product)